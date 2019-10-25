"""Exposes the user facing matchers for importing"""

from h_matchers.code import AnyFunction, AnyInstanceOf
from h_matchers.core import Matcher
from h_matchers.string import AnyString

__all__ = ["Any"]


class Any(Matcher):
    """A class that matches anything"""

    # pylint: disable=too-few-public-methods

    string = AnyString
    function = AnyFunction
    instance_of = AnyInstanceOf

    def __init__(self):
        super().__init__("* anything *", lambda _: True)
