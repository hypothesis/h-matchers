"""
A collection of flexible matchers for various collection types in a
fluent style.
"""
from h_matchers.core import Matcher


# Pylint doesn't understand this is a decorator
class fluent_entrypoint:  # pylint: disable=invalid-name
    """
    A decorator allowing a method on a class to act as either an instance
    method, or a class method (which will first create a blank instance of the
    class).
    """

    instance = None

    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        # If we have been called in a classmethod context, create a new
        # instance of the owning object
        if instance is None:
            instance = owner()
        self.instance = instance

        return self.__call__

    def __call__(self, *args, **kwargs):
        return self.function(self.instance, *args, **kwargs)


class AnyCollection(Matcher):
    """
    A versatile matcher for collections with a fluent style that can
    handle a range of different testing duties.
    """

    _exact_type = None
    _exact_size = None
    _min_size = None
    _max_size = None
    _items = None
    _item_matcher = None

    def __init__(self):
        # Pass None as our function, as we will be in charge of our own type
        # checking
        super().__init__("dummy", None)

    def __str__(self):
        parts = ["any"]
        if self._exact_type:
            parts.append(self._exact_type.__name__)
        else:
            parts.append("iterable")

        if self._exact_size:
            parts.append(f"of length {self._exact_size}")
        elif self._min_size is not None or self._max_size is not None:
            if self._min_size is not None and self._max_size is not None:
                parts.append(
                    f"with length between {self._min_size} and {self._max_size}"
                )
            elif self._min_size is not None:
                parts.append(f"with length > {self._min_size}")
            else:
                parts.append(f"with length < {self._max_size}")

        if self._items:
            parts.append(f"containing {self._items}")
            if self._items_are_ordered():
                parts.append("in order")

        if self._item_matcher:
            parts.append(f"of items matching {self._item_matcher}")

        return f'* {" ".join(parts)} *'

    @fluent_entrypoint
    def of_type(self, of_type):
        """
        Limit the type to a specific type like `list` or `set`.

        Can be called as an instance or class method.

        :return: self - for fluent chaining
        :rtype: AnyCollection
        """
        self._exact_type = of_type
        self._check_sort_type_agreement()

        return self

    @fluent_entrypoint
    def comprised_of(self, item_type):
        """
        Specify that every item in the iterable should match a single type.
        For example you can specify that the iterable contains only strings, or
        exactly the number '1'.

        Can be called as an instance or class method.

        :param item_type: The type to match again (can be another matcher)
        :return: self - for fluent chaining
        :rtype: AnyCollection
        """

        self._item_matcher = item_type
        return self

    @fluent_entrypoint
    def of_size(self, exact=None, at_least=None, at_most=None, strict=True):
        """
        Limit the size of the list.

        Can be called as an instance or class method.

        :param exact: Specify an exact size
        :param at_least: Specify a minimum size
        :param at_most: Specify a maximum size
        :param strict: Disallow 'None' for every field
        :raises ValueError: If arguments are missing or incompatible
        :return: self - for fluent chaining
        :rtype: AnyCollection
        """
        if strict and exact is None and at_least is None and at_most is None:
            raise ValueError("At least one option should not be None")

        if at_least is not None and at_most is not None:
            if at_least > at_most:
                raise ValueError("The upper bound must be higher than the lower bound")

            if at_least == at_most:
                exact = at_most
                at_most = at_least = None

        self._exact_size = exact
        self._min_size = at_least
        self._max_size = at_most

        return self

    @fluent_entrypoint
    def containing(self, items):
        """
        Specify that this item must contain these items. By default this
        is assumed to be in order. To change this you can call `in_any_order()`

        If a list of items is provided then these will be checked in order, if
        the comparison object supports ordering. If a set is provided the items
        will be checked in any order.

        Can be called as an instance or class method.

        :param items: A set or list of items to check for
        :return: self - for fluent chaining
        :raises ValueError: If you provide something other than a set or list
        :rtype: AnyCollection
        """
        if not isinstance(items, (set, list)):
            raise ValueError("Items must either be a list or set")

        self._items = items
        self._check_sort_type_agreement()

        return self

    @fluent_entrypoint
    def containing_exactly(self, items):
        """
        Specify this item must contain exactly the specified items. The semantics
        are the same as `containing()` except the lengths must match too.

        Can be called as an instance or class method.

        :param items: A set or list of items to check for
        :return: self - for fluent chaining
        :rtype: AnyCollection
        """
        self.containing(items)
        return self.of_size(len(items))

    def __eq__(self, other):
        if self._exact_type:
            if not isinstance(other, self._exact_type):
                return False
        elif not hasattr(other, "__iter__") and not hasattr(other, "__iter__"):
            return False

        # Take a copy in-case we were provided a generator. This lets us
        # exhaust it and then measure the size. This will fail for infinite
        # generators etc.
        copy = list(other)

        if not self._size_check(copy):
            return False

        if not self._item_type_check(copy, other):
            return False

        if not self._containment_check(copy):
            return False

        return True

    def _size_check(self, other):
        """Run the size check (if any)"""
        if self._exact_size is not None:
            return len(other) == self._exact_size

        if self._min_size and len(other) < self._min_size:
            return False

        if self._max_size and len(other) > self._max_size:
            return False

        return True

    def _check_sort_type_agreement(self):
        # We can't conflict if we don't have one side of the equation or other
        if self._items is None or not self._exact_type:
            return

        if self._items_are_ordered() and not self._our_type_supports_ordering():
            raise ValueError(
                f"Type {self._exact_type} does not sort ordered items. Use a set instead"
            )

    def _items_are_ordered(self):
        return isinstance(self._items, list)

    @classmethod
    def _supports_ordering(cls, item):
        return hasattr(item, "index")

    def _our_type_supports_ordering(self):
        return self._exact_type is None or self._supports_ordering(self._exact_type)

    def _containment_check(self, other):
        """Run the containment check (if any)"""
        if not self._items:
            return True

        found = [item for item in other if item in self._items]

        if self._our_type_supports_ordering() and self._items_are_ordered():
            return found == list(self._items)

        return set(found) == set(self._items)

    def _item_type_check(self, other, original):
        """
        Check to see if all items in the object match a particular pattern
        """
        if not self._item_matcher:
            return True

        if isinstance(original, dict):
            return all(value == self._item_matcher for value in original.keys())

        return all(item == self._item_matcher for item in other)


class AnyDict(AnyCollection):
    """A matcher representing any dict"""

    _exact_type = dict


class AnySet(AnyCollection):
    """A matcher representing any set."""

    _exact_type = set


class AnyList(AnyCollection):
    """A matcher representing any list."""

    _exact_type = list
