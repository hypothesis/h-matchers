import pytest
from tests.unit.data_types import DataTypes

from h_matchers.code import AnyFunction, AnyInstanceOfClass


class TestAnyInstanceOfClass:
    def test_it_matches(self):
        matcher = AnyInstanceOfClass(ValueError)
        assert ValueError() == matcher
        assert matcher == ValueError()

    @pytest.mark.parametrize("item,description", DataTypes.parameters())
    def test_it_does_not_match(self, item, description):
        matcher = AnyInstanceOfClass(ValueError)
        assert matcher != item
        assert item != matcher


class TestAnyFunction:
    @pytest.mark.parametrize(
        "item,description", DataTypes.parameters(exact=DataTypes.Groups.FUNCTIONS)
    )
    def test_it_matches(self, item, description):
        assert AnyFunction() == item
        assert item == AnyFunction()

    @pytest.mark.parametrize(
        "item,description", DataTypes.parameters(exclude=DataTypes.Groups.FUNCTIONS)
    )
    def test_it_does_not_match(self, item, description):
        assert AnyFunction() != item
        assert item != AnyFunction()
