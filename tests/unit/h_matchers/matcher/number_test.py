import pytest

from h_matchers.matcher.number import AnyComplex, AnyFloat, AnyInt
from tests.unit.data_types import DataTypes


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
