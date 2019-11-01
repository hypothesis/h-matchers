"""A collection of matchers for various number types."""

# pylint: disable=too-few-public-methods

from h_matchers.matcher.core import Matcher


class AnyInt(Matcher):
    """Matches any integer."""

    def __init__(self):
        super().__init__(
            "* any int *",
            lambda other: isinstance(other, int) and other is not True
            # pylint: disable=compare-to-zero
            and other is not False,
        )
