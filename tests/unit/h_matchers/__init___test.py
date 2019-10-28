import pytest
from tests.unit.data_types import DataTypes

from h_matchers import Any
from h_matchers.collection import AnyList, AnySet


class TestAnything:
    # pylint: disable=protected-access

    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_matches(self, item, _):
        assert Any() == item
        assert item == Any()

    @pytest.mark.parametrize(
        "attribute", ["instance_of", "string", "function", "callable", "list", "set"]
    )
    def test_it_has_expected_attributes(self, attribute):
        assert hasattr(Any, attribute)

    def test_it_provides_a_list_matcher(self):
        matcher = Any.list()
        assert isinstance(matcher, AnyList)

        matcher_fluent = Any.list.of_size(2)
        assert isinstance(matcher_fluent, AnyList)
        assert matcher_fluent._exact_size == 2

    def test_it_provides_a_set_matcher(self):
        matcher = Any.set()
        assert isinstance(matcher, AnySet)

        matcher_fluent = Any.set.of_size(2)
        assert isinstance(matcher_fluent, AnySet)
        assert matcher_fluent._exact_size == 2
