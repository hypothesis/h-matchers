"""
A collection of flexible matchers for various collection types in a
fluent style.
"""
from h_matchers.decorator import fluent_entrypoint
from h_matchers.matcher.core import Matcher
from h_matchers.unhashable_counter import UnhashableCounter


class NoMatch(ValueError):
    """The items do not match"""


class SizeMixin:
    _min_size = None
    _max_size = None

    @fluent_entrypoint
    def of_size(self, exact=None, at_least=None, at_most=None, strict=True):
        """Limit the size of the list.

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

    def _check_size(self, other):
        """Run the size check (if any)"""
        if self._min_size and len(other) < self._min_size:
            raise NoMatch("Too small")

        if self._max_size and len(other) > self._max_size:
            raise NoMatch("Too big")


class TypeMixin:
    _exact_type = None

    @fluent_entrypoint
    def of_type(self, of_type):
        """Limit the type to a specific type like `list` or `set`.

        Can be called as an instance or class method.

        :return: self - for fluent chaining
        :rtype: AnyCollection
        """
        self._exact_type = of_type

        return self

    def _check_type(self, other):
        if self._exact_type:
            if not isinstance(other, self._exact_type):
                raise NoMatch("Wrong type")

        elif not hasattr(other, "__iter__") and not hasattr(other, "__iter__"):
            raise NoMatch("Not iterable")

    def _type_supports_ordering(self):
        return self._exact_type is None or hasattr(self._exact_type, "index")


class ItemMatcherMixin:
    _item_matcher = None

    @fluent_entrypoint
    def comprised_of(self, item_type):
        """Specify that every item in the iterable should match a single type.

        For example you can specify that the iterable contains only strings, or
        exactly the number '1'.

        Can be called as an instance or class method.

        :param item_type: The type to match again (can be another matcher)
        :return: self - for fluent chaining
        :rtype: AnyCollection
        """

        self._item_matcher = item_type
        return self

    def _check_items_against_matcher(self, other, original):
        """Check to see if all items in the object match a particular pattern."""
        if not self._item_matcher:
            return

        items = original.keys() if isinstance(original, dict) else other

        for item in items:
            if not item == self._item_matcher:
                raise NoMatch("Item does not match item matcher")


class ContainmentMixin:
    _items = None
    _in_order = False
    _exact_match = False
    _item_counts = None

    @fluent_entrypoint
    def containing(self, items):
        """Specify that this item must contain these items.

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
        """Set that matched items can occur in any order.

        :raises ValueError: If no items have been set
        :rtype: AnyCollection
        """
        if self._items is None:
            raise ValueError("You must set items before calling this")

        self._in_order = True
        return self

    def only(self):
        """Set that only the provided items should be in the collection.

        :raises ValueError: If not items have been set
        :return: AnyCollection
        """
        if self._items is None:
            raise ValueError("You must set items before calling this")

        self._exact_match = True

        return self

    def _check_containment(self, other, ordered):
        if not self._items:
            return

        # We can bail out early if we need an exact match and they are
        # different sizes
        if self._exact_match and len(self._items) != len(other):
            raise NoMatch("Items of different size")

        if ordered and self._in_order:
            self._check_ordered_containment(other)
        else:
            self._check_unordered_containment(other)

    def _check_unordered_containment(self, other):
        """Check for items in this object out of order"""
        found_counts = UnhashableCounter(
            [item for item in other if item in self._items]
        )

        if self._exact_match:
            if found_counts != self._item_counts:
                raise NoMatch("Different item counts found")

        elif not found_counts >= self._item_counts:
            raise NoMatch("Could not find required item")

    def _check_ordered_containment(self, other):
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
                raise NoMatch("Could not find required item")


class AnyCollection(SizeMixin, TypeMixin, ItemMatcherMixin, ContainmentMixin, Matcher):
    """
    A versatile matcher for collections with a fluent style that can
    handle a range of different testing duties.
    """

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

    def __eq__(self, other):
        try:
            # Type checking only needs the original item
            self._check_type(other)

            # Take a copy in-case we were provided a generator. This lets us
            # exhaust it and then measure the size. This will fail for infinite
            # generators etc.
            copy = list(other)
            self._check_size(copy)
            self._check_items_against_matcher(copy, original=other)
            self._check_containment(copy, ordered=self._type_supports_ordering())

        except NoMatch:
            return False

        return True


class AnyDict(AnyCollection):
    """A matcher representing any dict"""

    _exact_type = dict


class AnySet(AnyCollection):
    """A matcher representing any set."""

    _exact_type = set


class AnyList(AnyCollection):
    """A matcher representing any list."""

    _exact_type = list
