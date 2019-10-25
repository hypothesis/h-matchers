import pytest
from tests.unit.data_types import DataTypes

from h_matchers.abstract import Anything


class TestAnything:
    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_matches(self, item, _):
        assert Anything() == item
        assert item == Anything()
