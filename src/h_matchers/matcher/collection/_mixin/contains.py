"""A mixin for AnyCollection which lets you check for specific items."""

from h_matchers.decorator import fluent_entrypoint
from h_matchers.exception import NoMatch
from h_matchers.matcher.collection.containment import (
    AnyIterableWithItems,
    AnyIterableWithItemsInOrder,
    AnyMappingWithItems,
)


class ContainsMixin:
    """Check specific items are in the container."""

    _items = None
    _in_order = False
    _exact_match = False

    @staticmethod
    def containing(items):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    # pylint: disable=function-redefined
    def containing(self, items):
        """Specify that this item must contain these items.

        By default we will attempt to match the items in any order.
        If you want to change this you can call `in_order()`.

        If a list of items is provided then these will be checked in order, if
        the comparison object supports ordering.

        If a dict of items is provided, then both the keys and values will be
        checked to see if they match.

        Can be called as an instance or class method.

        :param items: A set or list of items to check for
        :raises ValueError: If you provide something other than a set or list
        """

        if isinstance(items, ContainsMixin):
            # It's ok, because it's our class
            # pylint: disable=protected-access
            items = items._items

        self._items = items

    def in_order(self):
        """Set that matched items can occur in any order.

        :raises ValueError: If no items have been set
        :return: self - for fluent chaining
        """
        if self._items is None:
            raise ValueError("You must set items before calling this")

        self._in_order = True
        return self

    def only(self):
        """Set that only the provided items should be in the collection.

        :raises ValueError: If not items have been set
        :return: self - for fluent chaining
        """
        if self._items is None:
            raise ValueError("You must set items before calling this")

        self._exact_match = True

        return self

    def _check_contains(self, other, original=None):
        if not self._items:
            return

        # We can bail out early if we need an exact match and they are
        # different sizes
        if self._exact_match and len(self._items) != len(other):
            raise NoMatch("Items of different size")

        if hasattr(self._items, "items"):
            matcher_class = AnyMappingWithItems
        elif self._in_order:
            matcher_class = AnyIterableWithItemsInOrder
        else:
            matcher_class = AnyIterableWithItems

        if matcher_class(self._items) != original:
            raise NoMatch()

    def _describe_contains(self):
        if not self._items:
            return

        yield "containing"
        if self._exact_match:
            yield "only"

        yield f"{self._items}"

        if self._in_order:
            yield "in order"
