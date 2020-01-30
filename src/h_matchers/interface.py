"""The public interface class for comparing with things."""

from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.code import AnyCallable, AnyFunction, AnyInstanceOf
from h_matchers.matcher.collection import (
    AnyCollection,
    AnyDict,
    AnyList,
    AnyMapping,
    AnySet,
)
from h_matchers.matcher.combination import AllOf, AnyOf
from h_matchers.matcher.number import AnyInt
from h_matchers.matcher.string import AnyString
from h_matchers.matcher.url import AnyURL

# pylint: disable=too-few-public-methods

__all__ = ["Any", "All"]


class Any(AnyThing):
    """Matches anything and provides access to other matchers."""

    # pylint: disable=too-few-public-methods

    string = AnyString
    int = AnyInt

    function = AnyFunction
    callable = AnyCallable
    instance_of = AnyInstanceOf

    iterable = AnyCollection
    mapping = AnyMapping
    list = AnyList
    set = AnySet
    dict = AnyDict

    url = AnyURL

    of = AnyOf


class All(AllOf):
    """Matches when all items match.

    Mostly a sop to create a consistent interface.
    """

    of = AllOf
