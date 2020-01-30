import pytest

from h_matchers.interface import All, Any
from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.combination import AllOf


class TestAny:
    @pytest.mark.parametrize(
        "attribute",
        [
            "instance_of",
            "string",
            "function",
            "callable",
            "int",
            "iterable",
            "mapping",
            "list",
            "set",
            "dict",
            "of",
        ],
    )
    def test_it_has_expected_attributes(self, attribute):
        assert hasattr(Any, attribute)

    def test_is_subclass_of_AnyThing(self):
        assert issubclass(Any, AnyThing)


class TestAll:
    def test_it_has_expected_attributes(self):
        assert hasattr(All, "of")

    def test_is_subclass_of_AllOf(self):
        assert issubclass(All, AllOf)
