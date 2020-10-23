import pytest

from h_matchers.interface import All, Any
from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.combination import AllOf


class TestAny:
    @pytest.mark.parametrize(
        "attribute",
        [
            "callable",
            "complex",
            "dict",
            "float",
            "function",
            "generator",
            "instance_of",
            "int",
            "iterable",
            "list",
            "mapping",
            "object",
            "of",
            "request",
            "set",
            "string",
            "tuple",
            "url",
        ],
    )
    def test_it_has_expected_attributes(self, attribute):
        assert hasattr(Any, attribute)

    def test_is_subclass_of_AnyThing(self):
        assert issubclass(Any, AnyThing)

    def test_instance_of_is_not_singleton(self):
        # This is a regression test to ensure we don't have singleton like
        # behavior from Any.instance_of
        matcher = Any.instance_of(int)
        Any.instance_of(str)

        assert matcher == 1


class TestAll:
    def test_it_has_expected_attributes(self):
        assert hasattr(All, "of")

    def test_is_subclass_of_AllOf(self):
        assert issubclass(All, AllOf)
