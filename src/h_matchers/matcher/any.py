"""The public interface class for comparing with anything."""

from h_matchers.matcher.code import AnyCallable, AnyFunction, AnyInstanceOf
from h_matchers.matcher.collection import AnyCollection, AnyDict, AnyList, AnySet
from h_matchers.matcher.core import Matcher
from h_matchers.matcher.number import AnyInt
from h_matchers.matcher.string import AnyString

__all__ = ["Any"]


class Any(Matcher):
    """Matches anything and provides access to other matchers."""

    # pylint: disable=too-few-public-methods

    string = AnyString
    int = AnyInt

    function = AnyFunction
    callable = AnyCallable
    instance_of = AnyInstanceOf

    iterable = AnyCollection
    list = AnyList
    set = AnySet
    dict = AnyDict

    def __init__(self):
        super().__init__("* anything *", lambda _: True)
