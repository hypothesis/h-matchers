import pytest
from tests.unit.data_types import DataTypes

from h_matchers.matcher.code import AnyCallable, AnyFunction, AnyInstanceOf


class TestAnyInstanceOf:
    def test_it_matches(self):
        matcher = AnyInstanceOf(ValueError)
        assert ValueError() == matcher
        assert matcher == ValueError()

    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_does_not_match(self, item, _):
        matcher = AnyInstanceOf(ValueError)
        assert matcher != item
        assert item != matcher


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
