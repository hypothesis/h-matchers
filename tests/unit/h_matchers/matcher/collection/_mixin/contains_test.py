import pytest

from h_matchers.exception import NoMatch
from h_matchers.matcher.collection._mixin.contains import ContainsMixin


class HostClass(ContainsMixin):
    def __eq__(self, other):
        try:
            self._check_contains(list(other), other)

        except NoMatch:
            return False

        return True


class TestContainsMixin:
    def test_it_fails_in_order_with_no_items(self):
        with pytest.raises(ValueError):
            HostClass().in_order()

    def test_it_extracts_items_from_other_ContainsMixin_children(self):
        doner = HostClass.containing(["a", "b", "c"])

        recipient = HostClass.containing(doner)

        # pylint: disable=protected-access
        assert recipient._items == doner._items

    # Test delegation to matchers ------------------------------------------ #

    def test_it_delegates_to_AnyMappingWithItems_for_dicts(self, AnyMappingWithItems):
        items, other = {"a": 1}, {"b": 2}
        matcher = HostClass.containing(items)

        assert matcher != other

        self.assert_delegated(AnyMappingWithItems, items, other)

    def test_it_delegates_to_AnyIterableWithItemsInOrder_when_in_order(
        self, AnyIterableWithItemsInOrder
    ):
        items, other = ["a", 1], ["b", 2]
        matcher = HostClass.containing(items).in_order()

        assert matcher != other

        self.assert_delegated(AnyIterableWithItemsInOrder, items, other)

    def test_it_delegates_to_AnyIterableWithItems_when_out_of_order(
        self, AnyIterableWithItems
    ):
        items, other = ["a", 1], ["b", 2]
        matcher = HostClass.containing(items)

        assert matcher != other

        self.assert_delegated(AnyIterableWithItems, items, other)

    def assert_delegated(self, matcher_class, items, other):
        matcher_class.assert_called_once_with(items)
        try:
            matcher_class.return_value.__eq__.assert_called_once_with(other)
        except AssertionError:
            matcher_class.return_value.__ne__.assert_called_once_with(other)

    # Constraining to exact items ------------------------------------------ #

    def test_it_can_match_key_value_with_no_extras(self):
        matcher = HostClass.containing({"a": 1}).only()

        assert matcher == {"a": 1}
        assert matcher != {"a": 1, "b": 2}

    def test_it_can_match_in_order_with_no_extras(self):
        matcher = HostClass.containing([1, 1, 2]).only().in_order()

        assert matcher == [1, 1, 2]
        assert matcher != [0, 1, 2, 2]
        assert matcher != [1, 2, 2]

    def test_it_can_match_out_of_order_with_no_extras(self):
        matcher = HostClass.containing([1, 2]).only()

        assert matcher == [2, 1]
        assert matcher != [0, 1, 2]

    def test_only_fails_with_no_items(self):
        with pytest.raises(ValueError):
            HostClass().only()

    @pytest.fixture
    def AnyMappingWithItems(self, patch):
        return patch(
            "h_matchers.matcher.collection._mixin.contains.AnyMappingWithItems"
        )

    @pytest.fixture
    def AnyIterableWithItemsInOrder(self, patch):
        return patch(
            "h_matchers.matcher.collection._mixin.contains.AnyIterableWithItemsInOrder"
        )

    @pytest.fixture
    def AnyIterableWithItems(self, patch):
        return patch(
            "h_matchers.matcher.collection._mixin.contains.AnyIterableWithItems"
        )
