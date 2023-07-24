import pytest

from h_matchers import Any
from h_matchers.matcher.collection.containment import (
    AnyIterableWithItems,
    AnyIterableWithItemsInOrder,
    AnyMappingWithItems,
)
from tests.unit.data_types import DataTypes


class MultiDict(list):
    """Very bare bones implementation of a multi-dict."""

    def items(self):
        yield from self


class TestAnyMappableWithItems:
    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_fails_gracefully(self, item, _):
        assert item != AnyMappingWithItems({"a": 1})

    def test_it_can_match_values(self):
        matcher = AnyMappingWithItems({"a": 1})

        assert matcher == {"a": 1}
        assert {"a": 1} == matcher
        assert matcher == {"a": 1, "b": 2}

        assert {"a": 2} != matcher
        assert {"b": 2} != matcher

    def test_it_can_match_multi_dicts(self):
        multi_dict = MultiDict((("a", 2), ["a", 1], ("b", 2)))

        assert multi_dict == AnyMappingWithItems({"a": 2})
        assert multi_dict == AnyMappingWithItems({"a": 1})
        assert multi_dict == AnyMappingWithItems({"a": 1, "b": 2})
        assert multi_dict != AnyMappingWithItems({"d": 1})

    def test_it_can_match_with_multi_dicts(self):
        multi_dict = MultiDict((("a", 2), ["a", 1], ("b", 2)))

        matcher = AnyMappingWithItems(multi_dict)

        assert multi_dict == matcher
        assert {"a": 1, "b": 2} != matcher
        assert MultiDict((("a", 2), ["a", 1], ("b", 2), ["c", 3])) == matcher


class TestAnyIterableWithItemsInOrder:
    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_fails_gracefully(self, item, _):
        assert item != AnyIterableWithItemsInOrder(["a"])

    def test_it_matches_in_order(self):
        matcher = AnyIterableWithItemsInOrder([1, 1, 2])

        # Ordered things do
        assert matcher == [0, 1, 1, 2, 3]
        assert matcher == [2, 1, 1, 2, 3]  # It is in here
        assert matcher != [0, 2, 1, 1, 3]
        assert matcher != [1, 2, 2]

    def test_it_matches_generators_in_order(self):
        matcher = AnyIterableWithItemsInOrder([0, 1, 2])

        assert matcher == iter(range(3))
        assert iter(range(3)) == matcher

        assert matcher != iter(range(2))
        assert iter(range(2)) != matcher


class TestAnyIterableWithItems:
    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_fails_gracefully(self, item, _):
        assert item != AnyIterableWithItems(["a"])

    def test_it_matches_out_of_order(self):
        matcher = AnyIterableWithItems([1, 2])

        assert matcher == {2: "b", 1: "a", 0: "c"}
        assert matcher == {0, 2, 1}
        assert matcher == [0, 1, 2, 3]
        assert matcher == [0, 2, 1, 3]

        assert matcher != [1]
        assert matcher != [1, 1]

    def test_it_matches_generators_out_of_order(self):
        matcher = AnyIterableWithItems([2, 0, 1])

        def matching_gen():
            yield from range(3)

        assert matcher == matching_gen()
        assert matching_gen() == matcher

        def non_matching_gen():
            yield from range(2)

        assert matcher != non_matching_gen()
        assert non_matching_gen() != matcher

    def test_it_can_match_unhashable_in_any_order(self):
        dict_a = {"a": 1}
        dict_b = {"b": 2}
        matcher = AnyIterableWithItems([dict_a, dict_b])

        assert [dict_b, dict_a] == matcher
        assert matcher == [dict_b, dict_a]

    def test_it_matches_non_trival_matches(self):
        # For some items a naive approach will not work, as there are many
        # solutions to matching a set of objects, only some of which will
        # work.

        matcher = AnyIterableWithItems(
            [
                Any(),
                Any.string(),
                Any.string.containing("a"),
                Any.string.containing("aaaa"),
            ]
        )

        assert matcher == ["aaaa", "a", "", None]
        assert ["aaaa", "a", "", None] == matcher

    def test_it_detects_incompatible_matches(self):
        matcher = AnyIterableWithItems(
            [
                Any.string.containing("a"),
                Any.string.containing("a"),
                Any.string.containing("a"),
            ]
        )

        assert ["a", "aa", None] != matcher
        assert matcher != ["a", "aa", None]

    def test_it_remaps_matched_items(self):
        # This matcher will match against loads of things during the initial
        # constraint generation. We only want to see the final match
        sub_matcher = Any()
        matcher = AnyIterableWithItems([sub_matcher])

        assert matcher == [None, 1, "string"]

        # It's not clear our algorithm is deterministic, but hopefully the first
        # match is the one we'll hit.
        assert sub_matcher.matched_to == [None]
