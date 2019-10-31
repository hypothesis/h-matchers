"""Matchers for comparing to strings."""

# pylint: disable=too-few-public-methods

import re

from h_matchers.matcher.core import Matcher

__all__ = ["AnyString", "AnyStringContaining", "AnyStringMatching"]


class AnyStringContaining(Matcher):
    """Matches any string with a certain substring."""

    def __init__(self, sub_string):
        super().__init__(
            f"*{sub_string}*",
            lambda other: isinstance(other, str) and sub_string in other,
        )


class AnyStringMatching(Matcher):
    """Matches any regular expression."""

    def __init__(self, pattern, flags=0):
        """Create a string matcher with the specified regex.

        :param pattern: The raw pattern to compile into a regular expression
        :param flags: Flags `re` e.g. `re.IGNORECASE`
        """
        regex = re.compile(pattern, flags)
        super().__init__(
            pattern, lambda other: isinstance(other, str) and regex.match(other)
        )


class AnyString(Matcher):
    """Matches any string."""

    matching = AnyStringMatching
    containing = AnyStringContaining

    def __init__(self):
        super().__init__("* any string *", lambda other: isinstance(other, str))
