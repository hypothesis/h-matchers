"""A mixin for AnyCollection which adds checking all items with a matcher."""

# pylint: disable=too-few-public-methods

from h_matchers.decorator import fluent_entrypoint
from h_matchers.exception import NoMatch


class ItemMatcherMixin:
    """Check that all items in the object match an example."""

    _item_matcher = None

    @staticmethod
    def comprised_of(item_type):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    # pylint: disable=function-redefined
    def comprised_of(self, item_type):
        """Specify that every item in the iterable should match a single type.

        For example you can specify that the iterable contains only strings, or
        exactly the number '1'.

        Can be called as an instance or class method.

        :param item_type: The type to match again (can be another matcher)
        """

        self._item_matcher = item_type

    def _check_item_matcher(self, other, original):
        """Check to see if all items in the object match a pattern."""
        if not self._item_matcher:
            return

        items = original.keys() if isinstance(original, dict) else other

        for item in items:
            if not item == self._item_matcher:
                raise NoMatch("Item does not match item matcher")

    def _describe_item_matcher(self):
        if self._item_matcher:
            yield f"of items matching {self._item_matcher}"
