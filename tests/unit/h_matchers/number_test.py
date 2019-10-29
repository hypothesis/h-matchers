import pytest
from tests.unit.data_types import DataTypes

from h_matchers.matcher.number import AnyInt


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
