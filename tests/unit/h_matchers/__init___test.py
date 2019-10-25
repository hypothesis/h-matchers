import pytest
from tests.unit.data_types import DataTypes

from h_matchers import Any


class TestAnything:
    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_matches(self, item, _):
        assert Any() == item
        assert item == Any()

    @pytest.mark.parametrize("attribute", ["instance_of", "string", "function"])
    def test_it_has_expected_attributes(self, attribute):
        assert hasattr(Any, attribute)
