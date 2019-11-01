from h_matchers import Any
from h_matchers.matcher.collection.containment import (
    AnyIterableWithItems,
    AnyIterableWithItemsInOrder,
    AnyMappableWithItems,
)


class TestAnyMappableWithItems:
    def test_it_fails_gracefully(self):
        assert None != AnyMappableWithItems([])
        assert 5 != AnyMappableWithItems([])
        assert ValueError() != AnyMappableWithItems([])

    def test_it_can_match_values(self):
        matcher = AnyMappableWithItems({"a": 1})

        assert matcher == {"a": 1}
        assert {"a": 1} == matcher
        assert matcher == {"a": 1, "b": 2}

        assert {"a": 2} != matcher
        assert {"b": 2} != matcher


class TestAnyIterableWithItemsInOrder:
    def test_it_fails_gracefully(self):
        assert None != AnyIterableWithItemsInOrder([])
        assert 5 != AnyIterableWithItemsInOrder([])
        assert ValueError() != AnyIterableWithItemsInOrder([])

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
    def test_it_fails_gracefully(self):
        assert None != AnyIterableWithItems([])
        assert 5 != AnyIterableWithItems([])
        assert ValueError() != AnyIterableWithItems([])

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

        assert matcher == iter(range(3))
        assert iter(range(3)) == matcher

        assert matcher != iter(range(2))
        assert iter(range(2)) != matcher

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
