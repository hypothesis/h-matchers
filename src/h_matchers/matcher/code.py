"""Matchers for comparing to functions and classes etc."""

# pylint: disable=too-few-public-methods

from inspect import isclass

from h_matchers.matcher.core import Matcher

__all__ = ["AnyInstanceOf", "AnyFunction"]


class AnyInstanceOf(Matcher):
    """Matches any instance of another class."""

    def __init__(self, klass):
        super().__init__(klass.__name__, lambda other: isinstance(other, klass))


class AnyCallable(Matcher):
    """Matches any callable at all."""

    def __init__(self):
        super().__init__("* any callable *", callable)


class AnyFunction(Matcher):
    """Matches any function, but not classes."""

    def __init__(self):
        super().__init__(
            "* any function *", lambda item: callable(item) and not isclass(item)
        )
