"""
Classes implementing the matcher pattern for comparing to functions and
classes etc.
"""
# pylint: disable=too-few-public-methods

from inspect import isclass

from h_matchers.core import Matcher

__all__ = ["AnyInstanceOf", "AnyFunction"]


class AnyInstanceOf(Matcher):
    """A class that matches any instance of another class"""

    def __init__(self, klass):
        super().__init__(klass.__name__, lambda other: isinstance(other, klass))


class AnyFunction(Matcher):
    """A class that matches any function, but not classes"""

    def __init__(self):
        super().__init__(
            "* any function *", lambda item: callable(item) and not isclass(item)
        )
