"""The public interface class for comparing with things."""
from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.collection import (
    AnyCollection,
    AnyDict,
    AnyList,
    AnyMapping,
    AnySet,
)
from h_matchers.matcher.combination import AllOf, AnyOf
from h_matchers.matcher.meta import AnyCallable, AnyFunction
from h_matchers.matcher.number import AnyInt
from h_matchers.matcher.object import AnyObject
from h_matchers.matcher.strings import AnyString
from h_matchers.matcher.web.request import AnyRequest
from h_matchers.matcher.web.url import AnyURL

# pylint: disable=too-few-public-methods

__all__ = ["Any", "All"]


class Any(AnyThing):
    """Matches anything and provides access to other matchers."""

    # pylint: disable=too-few-public-methods

    string = AnyString
    int = AnyInt
    object = AnyObject

    function = AnyFunction
    callable = AnyCallable

    iterable = AnyCollection
    mapping = AnyMapping
    list = AnyList
    set = AnySet
    dict = AnyDict

    url = AnyURL
    request = AnyRequest

    of = AnyOf

    @staticmethod
    def instance_of(type_):
        """Specify that this item must be an instance of the provided type.

        :return: An instance of AnyObject configured with the given type.
        """
        return AnyObject.of_type(type_)


class All(AllOf):
    """Matches when all items match.

    Mostly a sop to create a consistent interface.
    """

    of = AllOf
