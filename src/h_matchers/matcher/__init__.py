"""Exposes the user facing matchers for importing"""

from h_matchers.matcher.code import AnyCallable, AnyFunction, AnyInstanceOf
from h_matchers.matcher.collection import AnyCollection, AnyDict, AnyList, AnySet
from h_matchers.matcher.core import Matcher
from h_matchers.matcher.number import AnyInt
from h_matchers.matcher.string import AnyString

__all__ = ["Any"]


class Any(Matcher):
    """A class that matches anything"""

    # pylint: disable=too-few-public-methods

    string = AnyString
    function = AnyFunction
    callable = AnyCallable
    instance_of = AnyInstanceOf

    iterable = AnyCollection
    list = AnyList
    set = AnySet
    dict = AnyDict

    int = AnyInt

    def __init__(self):
        super().__init__("* anything *", lambda _: True)
