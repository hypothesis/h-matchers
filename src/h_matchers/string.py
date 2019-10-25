"""Classes implementing the matcher pattern for comparing to strings"""
# pylint: disable=too-few-public-methods

import re

from h_matchers.core import Matcher

__all__ = ["AnyString", "AnyStringContaining", "AnyStringMatching"]


class AnyStringContaining(Matcher):
    """A class that matches any string with a certain substring"""

    def __init__(self, sub_string):
        super().__init__(
            f"*{sub_string}*",
            lambda other: isinstance(other, str) and sub_string in other,
        )


class AnyStringMatching(Matcher):
    """A class that matches any regular expression"""

    def __init__(self, pattern, flags=0):
        """
        :param pattern: The raw pattern to compile into a regular expression
        :param flags: Flags `re` e.g. `re.IGNORECASE`
        """
        regex = re.compile(pattern, flags)
        super().__init__(
            pattern, lambda other: isinstance(other, str) and regex.match(other)
        )


class AnyString(Matcher):
    """A class that matches any string"""

    matching = AnyStringMatching
    containing = AnyStringContaining

    def __init__(self):
        super().__init__("* any string *", lambda other: isinstance(other, str))
