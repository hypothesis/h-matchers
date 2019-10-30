import pytest
from tests.unit.data_types import DataTypes

from h_matchers.matcher import Any


class TestAnything:
    # pylint: disable=protected-access

    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_matches(self, item, _):
        assert Any() == item
        assert item == Any()

    @pytest.mark.parametrize(
        "attribute",
        ["instance_of", "string", "function", "callable", "list", "set", "int", "dict"],
    )
    def test_it_has_expected_attributes(self, attribute):
        assert hasattr(Any, attribute)