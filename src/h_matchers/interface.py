"""The public interface class for comparing with things."""

from h_matchers.matcher import collection
from h_matchers.matcher import number as _number
from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.combination import AllOf, AnyOf
from h_matchers.matcher.meta import AnyCallable, AnyFunction
from h_matchers.matcher.object import AnyObject
from h_matchers.matcher.strings import AnyString
from h_matchers.matcher.web.request import AnyRequest
from h_matchers.matcher.web.url import AnyURL

__all__ = ["Any", "All"]


class Any(AnyThing):
    """Matches anything and provides access to other matchers."""

    string = AnyString
    object = AnyObject

    number = _number.AnyReal
    int = _number.AnyInt
    float = _number.AnyFloat
    complex = _number.AnyComplex
    decimal = _number.AnyDecimal

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
