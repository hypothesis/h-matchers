"""Data types for testing the matchers."""

import enum
from decimal import Decimal


class _PrivateClass:
    """Represents a class."""

    @classmethod
    def class_method(cls):
        """Do nothing."""

    def instance_method(self):
        """Do nothing."""


def _function():
    """Do nothing."""


PRIVATE_CLASS = _PrivateClass()


class DataTypes(enum.Enum):
    """A collection of example data types to simplify writing unit-tests."""

    # The descriptions in the second position are mostly so Enum doesn't
    # equate things together and collapse our set of examples

    INT = (1, "integer")
    FALSY_INT = (0, "falsy integer")
    FLOAT = (1.0, "float")
    FALSY_FLOAT = (float(0), "falsy float")
    COMPLEX = (complex(1, 3.14159), "complex")
    FALSY_COMPLEX = (complex(0, 0), "falsy complex")
    DECIMAL = (Decimal(1), "decimal")
    FALSY_DECIMAL = (Decimal(0), "falsy decimal")

    TRUE = (True, "true")
    FALSE = (False, "false")

    STRING = ("string", "string")
    FALSY_STRING = ("", "falsy string")

    # This stuff is covered by iteration over the Enum in parameters()
    # but coverage can't tell because they aren't directly referenced

    LAMBDA = (lambda: 1, "lambda")  # pragma: no cover
    CLASS_METHOD = (_PrivateClass.class_method, "class method")  # pragma: no cover
    INSTANCE_METHOD = (
        PRIVATE_CLASS.instance_method,
        "instance method",
    )  # pragma: no cover
    BUILTIN_METHOD = (print, "built in")  # pragma: no cover
    FUNCTION = (_function, "function")  # pragma: no cover

    LIST = ([], "list")
    SET = (set(), "set")
    TUPLE = ((), "tuple")
    DICT = ({}, "dict")

    CLASS = (_PrivateClass, "class")  # pragma: no cover
    CLASS_INSTANCE = (PRIVATE_CLASS, "class instance")  # pragma: no cover
    PACKAGE = (enum, "package")  # pragma: no cover

    @classmethod
    def parameters(cls, exact=None, exclude=None):
        exclude = set(exclude or [])
        exact = exact or cls

        return (example.value for example in exact if example not in exclude)


class Groups:
    FUNCTIONS = {
        DataTypes.LAMBDA,
        DataTypes.CLASS_METHOD,
        DataTypes.INSTANCE_METHOD,
        DataTypes.BUILTIN_METHOD,
        DataTypes.FUNCTION,
    }

    CALLABLES = FUNCTIONS | {DataTypes.CLASS}

    STRINGS = {DataTypes.STRING, DataTypes.FALSY_STRING}

    INTS = {DataTypes.INT, DataTypes.FALSY_INT}
    FLOATS = {DataTypes.FLOAT, DataTypes.FALSY_FLOAT}
    COMPLEX = {DataTypes.COMPLEX, DataTypes.FALSY_COMPLEX}
    DECIMAL = {DataTypes.DECIMAL, DataTypes.FALSY_DECIMAL}
    NUMERIC = INTS | FLOATS | COMPLEX | DECIMAL
    REALS = INTS | FLOATS | DECIMAL

    ITERABLES = STRINGS | {
        DataTypes.LIST,
        DataTypes.SET,
        DataTypes.TUPLE,
        DataTypes.DICT,
    }


DataTypes.Groups = Groups
