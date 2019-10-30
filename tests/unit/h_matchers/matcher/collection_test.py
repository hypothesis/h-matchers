import pytest
from tests.unit.data_types import DataTypes

from h_matchers import Any
from h_matchers.matcher.collection import AnyCollection


class TestAnyCollection:
    # pylint: disable=protected-access

    # Test type matching ------------------------------------------------- #

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.ITERABLES)
    )
    def test_it_matches(self, item, _):
        assert AnyCollection() == item
        assert item == AnyCollection()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.ITERABLES)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyCollection() != item
        assert item != AnyCollection()

    def test_it_matches_specific_class(self):
        matcher = AnyCollection().of_type(list)

        assert matcher == []
        assert [] == matcher
        assert matcher != set()
        assert set() != matcher

    # Size matching -------------------------------------------------------- #

    def test_it_matches_exact_size(self):
        matcher = AnyCollection().of_size(3)

        assert matcher == [1, 2, 3]
        assert {1, 2, 3} == matcher
        assert matcher != set()
        assert matcher != [1, 2]

    def test_it_matches_minimum_size(self):
        matcher = AnyCollection().of_size(at_least=2)

        assert matcher == [1, 2]
        assert matcher == [1, 2, 3]
        assert matcher != [1]

    def test_it_complains_with_incorrect_size(self):
        with pytest.raises(ValueError):
            AnyCollection().of_size()

        with pytest.raises(ValueError):
            AnyCollection().of_size(at_least=100, at_most=1)

    def test_it_matches_maximum_size(self):
        matcher = AnyCollection().of_size(at_most=2)

        assert matcher == []
        assert matcher == [1, 2]
        assert matcher != [1, 2, 3]

    # Any order comparison ------------------------------------------------- #

    def test_it_matches_out_of_order(self):
        matcher = AnyCollection().containing([1, 2])

        assert matcher == {2: "b", 1: "a", 0: "c"}
        assert matcher == {0, 2, 1}
        assert matcher == [0, 1, 2, 3]
        assert matcher == [0, 2, 1, 3]

    def test_it_matches_out_of_order_with_exact_items(self):
        matcher = AnyCollection().containing([1, 1, 2]).only()

        assert matcher == [2, 1, 1]

        assert matcher != [1, 2, 2]
        assert matcher != {1, 2}
        assert matcher != {2: "b", 1: "a"}

    def test_it_can_match_unhashable_in_any_order(self):
        dict_a = {"a": 1}
        dict_b = {"b": 2}
        matcher = AnyCollection().containing([dict_a, dict_b])

        assert [dict_b, dict_a] == matcher
        assert matcher == [dict_b, dict_a]

    def test_it_matches_generators_in_order(self):
        matcher = AnyCollection().containing([0, 1, 2]).only().in_order()

        assert matcher == iter(range(3))
        assert iter(range(3)) == matcher

        non_matcher = AnyCollection().containing([2, 1, 0]).only().in_order()
        assert non_matcher != iter(range(3))
        assert iter(range(3)) != non_matcher

    # In order item comparison --------------------------------------------- #

    def test_it_matches_in_order(self):
        matcher = AnyCollection().containing([1, 1, 2]).in_order()

        # Ordered things do
        assert matcher == [0, 1, 1, 2, 3]
        assert matcher == [2, 1, 1, 2, 3]  # It is in here
        assert matcher != [0, 2, 1, 1, 3]
        assert matcher != [1, 2, 2]

    def test_it_matches_in_order_with_exact_items(self):
        matcher = AnyCollection().containing([1, 1, 2]).only().in_order()

        assert matcher == [1, 1, 2]
        assert matcher != [0, 1, 2, 2]
        assert matcher != [1, 2, 2]

    def test_it_fails_in_order_with_no_items(self):
        with pytest.raises(ValueError):
            AnyCollection().in_order()

    def test_it_matches_generators_out_of_order(self):
        matcher = AnyCollection().containing([2, 0, 1]).only()

        assert matcher == iter(range(3))
        assert iter(range(3)) == matcher
        assert iter(range(4)) != matcher

    # Constraining to exact items ------------------------------------------ #

    def test_it_can_constrain_to_exact_matching(self):
        matcher = AnyCollection().containing({1, 2}).only()

        assert matcher == {2: "b", 1: "a"}
        assert matcher == {2, 1}
        assert matcher == [1, 2]

        assert matcher != {2: "b", 1: "a", 0: "c"}
        assert {1} != matcher
        assert matcher != [0, 1, 2, 3]

    def test_only_fails_with_no_items(self):
        with pytest.raises(ValueError):
            AnyCollection().only()

    # Other ---------------------------------------------------------------- #

    def test_it_can_apply_a_matcher_to_all_elements(self):
        matcher = AnyCollection().comprised_of(Any.string())

        assert matcher == ["a", "b"]
        assert matcher == {"a": 1, "b": 2}

        assert matcher != ["a", "b", 1]
        assert matcher != {"a": 1, "b": 1, 3: None}

    @pytest.mark.parametrize(
        "matcher,expected",
        (
            (AnyCollection(), "any iterable"),
            (AnyCollection().of_type(list), "any list"),
            (AnyCollection().of_size(5), "length 5"),
            (AnyCollection().of_size(at_least=4), "length > 4"),
            (AnyCollection().of_size(at_most=3), "length < 3"),
            (AnyCollection().of_size(at_least=2, at_most=7), "length between 2 and 7"),
            (AnyCollection().containing({1, 2}), "containing {1, 2}"),
            (
                AnyCollection().containing([1, 2]).in_order(),
                "containing [1, 2] in order",
            ),
            (AnyCollection().containing([1, 2]).only(), "containing only [1, 2]"),
            (AnyCollection().comprised_of(1), "of items matching 1"),
        ),
    )
    def test_it_stringifies_well(self, matcher, expected):
        assert str(matcher) == Any.string.containing(expected)

    def test_you_can_use_fluent_style_for_first_element(self):
        matcher = AnyCollection.of_size(2).containing([1, 2]).of_type(list)

        assert isinstance(matcher, AnyCollection)
        assert matcher._min_size == 2
        assert matcher._items == [1, 2]
        assert matcher._exact_type == list
