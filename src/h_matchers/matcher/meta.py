"""Matchers for comparing to functions and classes etc."""

# pylint: disable=too-few-public-methods

from inspect import isclass

from h_matchers.matcher.core import Matcher

__all__ = ["AnyCallable", "AnyFunction"]


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
