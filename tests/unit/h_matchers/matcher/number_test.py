import pytest

from h_matchers.matcher.number import (
    AnyComplex,
    AnyDecimal,
    AnyFloat,
    AnyInt,
    AnyNumber,
    AnyReal,
)
from tests.unit.data_types import DataTypes


class TestAnyNumber:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.NUMERIC)
    )
    def test_it_matches(self, item, _):
        assert AnyNumber() == item
        assert item == AnyNumber()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.NUMERIC)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyNumber() != item
        assert item != AnyNumber()

    @pytest.mark.parametrize(
        "value,matcher,should_match",
        (
            (4, AnyNumber().not_equal_to(4), False),
            (3, AnyNumber().not_equal_to(4), True),
            (1, AnyNumber().truthy(), True),
            (0, AnyNumber().truthy(), False),
            (1, AnyNumber().falsy(), False),
            (0, AnyNumber().falsy(), True),
        ),
    )
    def test_comparators(self, value, matcher, should_match):
        assert bool(value == matcher) == should_match
        assert bool(matcher == value) == should_match

    @pytest.mark.parametrize(
        "matcher,string",
        (
            (AnyNumber(), "** any number **"),
            (AnyNumber().truthy(), "** any number, truthy **"),
            (
                AnyNumber().not_equal_to(4).truthy().falsy(),
                "** any number, != 4, truthy, and falsy **",
            ),
        ),
    )
    def test___str__(self, matcher, string):
        assert str(matcher) == string


class TestAnyInt:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.INTS)
    )
    def test_it_matches(self, item, _):
        assert AnyInt() == item
        assert item == AnyInt()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.INTS)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyInt() != item
        assert item != AnyInt()

    @pytest.mark.parametrize(
        "value,matcher,should_match",
        (
            (3, AnyInt() > 2, True),
            (2, AnyInt() > 2, False),
            (1, AnyInt() > 2, False),
            (3, AnyInt().greater_than(2), True),
            (2, AnyInt().greater_than(2), False),
            (1, AnyInt().greater_than(2), False),
            (3, AnyInt() >= 2, True),
            (2, AnyInt() >= 2, True),
            (1, AnyInt() >= 2, False),
            (3, AnyInt().greater_than_or_equal_to(2), True),
            (2, AnyInt().greater_than_or_equal_to(2), True),
            (1, AnyInt().greater_than_or_equal_to(2), False),
            (3, AnyInt() < 2, False),
            (2, AnyInt() < 2, False),
            (1, AnyInt() < 2, True),
            (3, AnyInt().less_than(2), False),
            (2, AnyInt().less_than(2), False),
            (1, AnyInt().less_than(2), True),
            (3, AnyInt() <= 2, False),
            (2, AnyInt() <= 2, True),
            (1, AnyInt() <= 2, True),
            (3, AnyInt().less_than_or_equal_to(2), False),
            (2, AnyInt().less_than_or_equal_to(2), True),
            (1, AnyInt().less_than_or_equal_to(2), True),
            (4, AnyInt().multiple_of(2), True),
            (3, AnyInt().multiple_of(2), False),
            (4, AnyInt().even(), True),
            (3, AnyInt().even(), False),
            (4, AnyInt().odd(), False),
            (3, AnyInt().odd(), True),
        ),
    )
    def test_comparators(self, value, matcher, should_match):
        assert bool(value == matcher) == should_match
        assert bool(matcher == value) == should_match


class TestAnyReal:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.REALS)
    )
    def test_it_matches(self, item, _):
        assert AnyReal() == item
        assert item == AnyReal()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.REALS)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyReal() != item
        assert item != AnyReal()

    @pytest.mark.parametrize(
        "value,matcher,should_match",
        (
            (4, AnyReal().approximately(4), True),
            (4.0001, AnyReal().approximately(4), True),
            (4.3, AnyReal().approximately(4), False),
            (4.3, AnyReal().approximately(4, 0.4), True),
        ),
    )
    def test_comparators(self, value, matcher, should_match):
        assert bool(value == matcher) == should_match
        assert bool(matcher == value) == should_match


class TestAnyFloat:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.FLOATS)
    )
    def test_it_matches(self, item, _):
        assert AnyFloat() == item
        assert item == AnyFloat()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.FLOATS)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyFloat() != item
        assert item != AnyFloat()


class TestAnyComplex:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.COMPLEX)
    )
    def test_it_matches(self, item, _):
        assert AnyComplex() == item
        assert item == AnyComplex()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.COMPLEX)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyComplex() != item
        assert item != AnyComplex()


class TestAnyDecimal:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.DECIMAL)
    )
    def test_it_matches(self, item, _):
        assert AnyDecimal() == item
        assert item == AnyDecimal()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.DECIMAL)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyDecimal() != item
        assert item != AnyDecimal()
