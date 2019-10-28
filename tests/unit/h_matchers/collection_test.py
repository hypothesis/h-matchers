import pytest
from tests.unit.data_types import DataTypes

from h_matchers import Any
from h_matchers.collection import AnyCollection


class TestAnyCollection:
    # pylint: disable=protected-access

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

    def test_it_sets_exact_with_exact_boundaries(self):
        matcher = AnyCollection().of_size(at_most=10, at_least=10)
        assert matcher._exact_size == 10
        assert matcher._min_size is None
        assert matcher._max_size is None

    def test_it_matches_maximum_size(self):
        matcher = AnyCollection().of_size(at_most=2)

        assert matcher == []
        assert matcher == [1, 2]
        assert matcher != [1, 2, 3]

    def test_it_tests_containment_in_order(self):
        matcher = AnyCollection().containing([1, 2])

        # Ordered things do
        assert matcher == [0, 1, 2, 3]
        assert matcher != [0, 2, 1, 3]

        # Un-ordered things can't be compared to ordered items
        with pytest.raises(ValueError):
            assert matcher != {2: "b", 1: "a", 0: "c"}
        with pytest.raises(ValueError):
            assert matcher != {0, 2, 1}

    def test_it_tests_containment_in_any_order(self):
        matcher = AnyCollection().containing({1, 2})

        assert matcher == {2: "b", 1: "a", 0: "c"}
        assert matcher == {0, 2, 1}
        assert matcher == [0, 1, 2, 3]
        assert matcher == [0, 2, 1, 3]

    def test_it_tests_containment_and_length(self):
        matcher = AnyCollection().containing_exactly({1, 2})

        assert matcher == {2: "b", 1: "a"}
        assert matcher == {2, 1}
        assert matcher == [1, 2]

        assert matcher != {2: "b", 1: "a", 0: "c"}
        assert matcher != {0, 2, 1}
        assert matcher != [0, 1, 2, 3]

    def test_it_matches_item_type(self):
        matcher = AnyCollection().comprised_of(Any.string())

        assert matcher == ["a", "b"]
        assert matcher == {1: "a", 2: "b"}

        assert matcher != ["a", "b", 1]
        assert matcher != {1: "a", 2: "b", 3: None}

    def test_items_must_be_lists_or_dicts(self):
        with pytest.raises(ValueError):
            AnyCollection().containing({"a": 1})

    def test_items_must_agree_with_type(self):
        assert AnyCollection().containing([])
        assert AnyCollection().containing(set())
        assert AnyCollection().of_type(list).containing([])

        with pytest.raises(ValueError):
            AnyCollection().of_type(set).containing([])

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
            (AnyCollection().containing([1, 2]), "containing [1, 2] in order"),
            (AnyCollection().comprised_of(1), "of items matching 1"),
        ),
    )
    def test_stringification(self, matcher, expected):
        assert str(matcher) == Any.string.containing(expected)

    def test_fluent_entry(self):
        matcher = AnyCollection.of_size(2).containing([1, 2]).of_type(list)

        assert isinstance(matcher, AnyCollection)
        assert matcher._exact_size == 2
        assert matcher._items == [1, 2]
        assert matcher._exact_type == list
