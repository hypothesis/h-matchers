"""Matchers for simple objects."""
from h_matchers.decorator import fluent_entrypoint
from h_matchers.matcher.core import Matcher

# pylint: disable=function-redefined


class AnyObject(Matcher):  # pragma: no cover
    """Match any object, optionally with a specific class or attributes.

    It's possible to instantiate this object without specifying a type or any
    attributes, but as most everything is an object in Python 3, this is
    largely equivalent to an `Any()` matcher.

    Any specified attributes must be present on the object being compared to,
    and must have matching values. It's is possible to nest matchers if you
    require an attribute to be present, but not have any particular value:

        AnyObject.with_attrs({"name": Any()})

    Any attributes specified will be available as attributes on the matcher
    object. This is helpful if you need to sort the items before comparing them
    for example.
    """

    def __init__(self, type_=None, attributes=None):
        """Create a new object matcher.

        :param type_: The type this object will match
        :param attributes:  A mapping of attributes to values to match
        """
        # Use scrambled names to reduce the chances of attribute clashes
        self.__type = type_
        self.__attributes = attributes

        super().__init__("dummy", self._matches_object)

    @staticmethod
    def of_type(type_):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    def of_type(self, type_):
        """Specify that this item must be an instance of the provided type.

        Can be called as an instance or class method.

        :param type_: The type this object will match
        """
        self.__type = type_

    @staticmethod
    def with_attrs(attributes):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    def with_attrs(self, attributes):
        """Specify that this item must have at least these attribute values.

        Takes a mapping containing the names of attributes that the target
        object must have, and values that those values must take.

        Any attributes specified this way are accessible on this matcher as
        attributes, unless they clash with methods of this class.

        Can be called as an instance or class method.

        :param attributes: A mapping of attributes to values
        :raise ValueError: If the provided attributes do not support `items()`
        """
        if not hasattr(attributes, "items"):
            raise ValueError("The attributes must be a mapping")

        self.__attributes = attributes

    def _matches_object(self, other):
        if self.__type is not None and not isinstance(other, self.__type):
            return False

        if self.__attributes is not None:
            for key, value in self.__attributes.items():
                if not hasattr(other, key):
                    return False

                if getattr(other, key) != value:
                    return False

        return True

    def __getattr__(self, item):
        """Allow our attributes spec to be accessed as attributes."""

        if self.__attributes is not None and item in self.__attributes:
            return self.__attributes[item]

        return super().__getattribute__(item)

    def __str__(self):
        extras = f" with attributes {self.__attributes}" if self.__attributes else ""

        instance = object.__name__ if self.__type is None else self.__type.__name__

        return f"<Any instance of '{instance}'{extras}>"
