"""A matcher that matches anything."""
from h_matchers.matcher.core import Matcher

# pylint: disable=too-few-public-methods


class AnyThing(Matcher):
    """Matches anything."""

    def __init__(self):
        super().__init__("* anything *", lambda _: True)
