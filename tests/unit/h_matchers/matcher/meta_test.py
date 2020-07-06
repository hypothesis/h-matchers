import pytest

from h_matchers.matcher.meta import AnyCallable, AnyFunction
from tests.unit.data_types import DataTypes


class TestAnyFunction:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.FUNCTIONS)
    )
    def test_it_matches(self, item, _):
        assert AnyFunction() == item
        assert item == AnyFunction()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.FUNCTIONS)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyFunction() != item
        assert item != AnyFunction()


class TestAnyCallable:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.CALLABLES)
    )
    def test_it_matches(self, item, _):
        assert AnyCallable() == item
        assert item == AnyCallable()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.CALLABLES)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyCallable() != item
        assert item != AnyCallable()
