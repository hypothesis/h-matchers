"""A collection of matchers for various number types."""

# pylint: disable=too-few-public-methods
from decimal import Decimal

from h_matchers.matcher.core import Matcher


class AnyNumber(Matcher):
    _types = (int, float, complex, Decimal)
    _type_description = "number"

    def __init__(self):
        super().__init__("dummy", self.assert_equal_to)

    def assert_equal_to(self, other):
        # Ints are also booleans
        # pylint: disable=compare-to-zero
        assert other is not True and other is not False, "Not a boolean"

        # Check it's the right type
        assert isinstance(other, self._types)

        return True

    def __str__(self):
        return f"** any {self._type_description} **"


class AnyInt(AnyNumber):
    """Matches any integer."""

    _types = (int,)
    _type_description = "integer"


class AnyFloat(AnyNumber):
    """Matches any float."""

    _types = (float,)
    _type_description = "float"


class AnyComplex(AnyNumber):
    """Matches any complex number."""

    _types = (complex,)
    _type_description = "complex"
