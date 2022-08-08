import pytest

from h_matchers.matcher.anything import AnyThing
from tests.unit.data_types import DataTypes


class TestAnything:
    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_matches(self, item, _):
        assert AnyThing() == item
        assert item == AnyThing()
