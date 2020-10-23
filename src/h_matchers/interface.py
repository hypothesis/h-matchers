"""The public interface class for comparing with things."""
from h_matchers.matcher import collection, number
from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.combination import AllOf, AnyOf
from h_matchers.matcher.meta import AnyCallable, AnyFunction
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
    object = AnyObject

    int = number.AnyInt
    float = number.AnyFloat
    complex = number.AnyComplex

    function = AnyFunction
    callable = AnyCallable

    mapping = collection.AnyMapping
    dict = collection.AnyDict

    iterable = collection.AnyCollection
    list = collection.AnyList
    set = collection.AnySet
    tuple = collection.AnyTuple
    generator = collection.AnyGenerator

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
