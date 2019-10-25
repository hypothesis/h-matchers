"""
Abstract or combinatorial matchers.
"""
# pylint: disable=too-few-public-methods

from h_matchers.core import LambdaMatcher


class Anything(LambdaMatcher):
    """A class that matches anything"""

    def __init__(self):
        super().__init__("* anything *", lambda _: True)
