from unittest.mock import Mock, create_autospec

import pytest
from tests.unit.data_types import DataTypes

from h_matchers import Any
from h_matchers.exception import NoMatch
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

    # Other ---------------------------------------------------------------- #

    def test_it_uses_the_mixins_for_equality_tests(self, TestableAnyCollection):
        matcher = TestableAnyCollection()

        other = {1, 2}
        list_other = list(other)

        assert matcher == other

        matcher._check_type.assert_called_once_with(matcher, list_other, other)
        matcher._check_size.assert_called_once_with(matcher, list_other, other)
        matcher._check_item_matcher.assert_called_once_with(matcher, list_other, other)
        matcher._check_contains.assert_called_once_with(matcher, list_other, other)

    def test_it_respects_the_mixins_raising_NoMatch(self, TestableAnyCollection):
        matcher = TestableAnyCollection()
        matcher._check_type = Mock(side_effect=NoMatch())

        assert matcher != []

    @pytest.fixture
    def TestableAnyCollection(self):
        class TestableAnyCollection(AnyCollection):
            _check_type = create_autospec(AnyCollection._check_type)
            _check_size = create_autospec(AnyCollection._check_size)
            _check_item_matcher = create_autospec(AnyCollection._check_item_matcher)
            _check_contains = create_autospec(AnyCollection._check_contains)

        return TestableAnyCollection

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
