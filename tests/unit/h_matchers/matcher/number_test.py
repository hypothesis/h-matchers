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
