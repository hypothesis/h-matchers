"""
A collection of flexible matchers for various collection types in a
fluent style.
"""
from h_matchers.matcher.core import Matcher
from h_matchers.decorator import fluent_entrypoint
from h_matchers.unhashable_counter import UnhashableCounter


class AnyCollection(Matcher):
    """
    A versatile matcher for collections with a fluent style that can
    handle a range of different testing duties.
    """

    _exact_type = None
    _min_size = None
    _max_size = None
    _items = None
    _item_matcher = None
    _in_order = False
    _exact_match = False
    _item_counts = None

    def __init__(self):
        # Pass None as our function, as we will be in charge of our own type
        # checking
        super().__init__("dummy", None)

    def __str__(self):
        # This is some pretty gross code, but it makes test output so much
        # more readable
        parts = ["any"]
        if self._exact_type:
            parts.append(self._exact_type.__name__)
        else:
            parts.append("iterable")

        if self._min_size is not None or self._max_size is not None:
            if self._min_size == self._max_size:
                parts.append(f"of length {self._min_size}")
            elif self._min_size is not None and self._max_size is not None:
                parts.append(
                    f"with length between {self._min_size} and {self._max_size}"
                )
            elif self._min_size is not None:
                parts.append(f"with length > {self._min_size}")
            else:
                parts.append(f"with length < {self._max_size}")

        if self._items:
            parts.append("containing")
            if self._exact_match:
                parts.append("only")

            parts.append(f"{self._items}")

            if self._in_order:
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
        if exact is not None:
            self._min_size = exact
            self._max_size = exact

        elif strict and at_least is None and at_most is None:
            raise ValueError("At least one option should not be None")

        else:
            if at_least is not None and at_most is not None and at_least > at_most:
                raise ValueError("The upper bound must be higher than the lower bound")

            self._min_size = at_least
            self._max_size = at_most

        return self

    @fluent_entrypoint
    def containing(self, items):
        """
        Specify that this item must contain these items.

        By default we will attempt to match the items in any order.
        If you want to change this you can call `in_order()`.

        If a list of items is provided then these will be checked in order, if
        the comparison object supports ordering. If a set is provided the items
        will be checked in any order.

        Can be called as an instance or class method.

        :param items: A set or list of items to check for
        :raises ValueError: If you provide something other than a set or list
        :return: self - for fluent chaining
        :rtype: AnyCollection
        """

        self._items = items
        self._item_counts = UnhashableCounter(items)

        return self

    def in_order(self):
        """
        Set that matched items can occur in any order
        :raises ValueError: If no items have been set
        :rtype: AnyCollection
        """
        if self._items is None:
            raise ValueError("You must set items before calling this")

        self._in_order = True
        return self

    def only(self):
        if self._items is None:
            raise ValueError("You must set items before calling this")

        self._exact_match = True
        self.of_size(len(self._items))

        return self

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
        if self._min_size and len(other) < self._min_size:
            return False

        if self._max_size and len(other) > self._max_size:
            return False

        return True

    def _our_type_supports_ordering(self):
        return self._exact_type is None or hasattr(self._exact_type, "index")

    def _containment_check(self, other):
        """Run the containment check (if any)"""
        if not self._items:
            return True

        if self._our_type_supports_ordering() and self._in_order:
            return self._ordered_containment_check(other)

        return self._unordered_containment_check(other)

    def _unordered_containment_check(self, other):
        """Check for items in this object out of order"""
        found_counts = UnhashableCounter(
            [item for item in other if item in self._items]
        )

        if self._exact_match:
            return found_counts == self._item_counts

        return found_counts >= self._item_counts

    def _ordered_containment_check(self, other):
        """Check for items in this object in order"""
        last_index = None

        for item in self._items:
            try:
                last_index = (
                    other.index(item)
                    if last_index is None
                    else other.index(item, last_index)
                ) + 1
            except ValueError:
                return False

        return True

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
