from collections import namedtuple

import pytest
from _pytest.mark import param

from h_matchers import Any
from h_matchers.matcher.object import AnyObject

ValueObject = namedtuple("ValueObject", ["one", "two"])
NotValueObject = namedtuple("NotValueObject", ["one", "two"])


class TestAnyObject:
    @pytest.mark.parametrize(
        "type_,instance,matches",
        (
            # If you don't specify, we really don't care
            (None, object(), True),
            (None, ValueError(), True),
            (None, 1, True),
            # Actual classes to test for
            param(ValueError, ValueError(), True, id="Exact class ok"),
            param(BaseException, ValueError(), True, id="Subclass ok"),
            param(ValueError, object(), False, id="Superclass not ok"),
            param(ValueError, IndexError, False, id="Different class not ok"),
        ),
    )
    def test_it_matches_types_correctly(self, type_, instance, matches):
        matcher = AnyObject(type_=type_)

        if matches:
            assert instance == matcher
            assert matcher.assert_equal_to(instance)
        else:
            assert instance != matcher
            with pytest.raises(AssertionError):
                matcher.assert_equal_to(instance)

    @pytest.mark.parametrize(
        "attributes,matches",
        (
            ({"one": "one", "two": "two"}, True),
            ({"one": "one"}, True),
            ({"one": Any()}, True),
            ({}, True),
            ({"one": "one", "not_an_attr": ""}, False),
            ({"one": "BAD", "two": "two"}, False),
        ),
    )
    def test_it_matches_with_attributes_correctly(self, attributes, matches):
        other = ValueObject(one="one", two="two")
        matcher = AnyObject.with_attrs(attributes)

        if matches:
            assert other == matcher
            assert matcher.assert_equal_to(other)
        else:
            assert other != matcher
            with pytest.raises(AssertionError):
                matcher.assert_equal_to(other)

    @pytest.mark.parametrize("bad_input", (None, 1, []))
    def test_it_raise_ValueError_if_attributes_does_not_support_items(self, bad_input):
        with pytest.raises(ValueError):
            AnyObject.with_attrs(bad_input)

    def test_it_mocks_attributes(self):
        matcher = AnyObject.with_attrs({"a": "A"})

        assert matcher.a == "A"

        with pytest.raises(AttributeError):
            matcher.b  # pylint: disable=pointless-statement

    @pytest.mark.parametrize(
        "magic_method",
        [
            # All the magic methods we rely on post init
            "__eq__",
            "__getattr__",
            "__str__",
        ],
    )
    def test_setting_magic_methods_as_attributes_does_not_set_attributes(
        self, magic_method
    ):
        # There's no sensible reason to do it, but we should still be able to
        # function normally if you do.

        weird_matcher = AnyObject.with_attrs({magic_method: "test"})

        result = getattr(weird_matcher, magic_method)

        assert callable(result)

    def test_type_and_attributes_at_once(self):
        matcher = AnyObject.of_type(ValueObject).with_attrs({"one": "one"})

        assert ValueObject("one", "two") == matcher
        assert NotValueObject("one", "two") != matcher
        assert ValueObject("bad", "two") != matcher

    @pytest.mark.parametrize(
        "type_,attributes,string",
        (
            (None, None, "<Any instance of 'object'>"),
            (ValueObject, None, "<Any instance of 'ValueObject'>"),
            (None, {"a": "b"}, "<Any instance of 'object' with attributes {'a': 'b'}>"),
            (
                ValueObject,
                {"a": "b"},
                "<Any instance of 'ValueObject' with attributes {'a': 'b'}>",
            ),
        ),
    )
    def test_stringification(self, type_, attributes, string):
        matcher = AnyObject(type_=type_, attributes=attributes)

        assert str(matcher) == string
