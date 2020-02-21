"""Matchers formed of combinations of other things."""
from h_matchers.matcher.core import Matcher

# pylint: disable=too-few-public-methods


class AnyOf(Matcher):
    """Match any one of a series of options."""

    def __init__(self, options):
        options = list(options)  # Coerce generators into concrete list

        super().__init__(
            f"* any of {options} *", lambda other: other in options,
        )


class AllOf(Matcher):
    """Match only when all of a series of options match."""

    def __init__(self, options):
        options = list(options)  # Coerce generators into concrete list

        super().__init__(
            f"* all of {options} *",
            lambda other: all(other == option for option in options),
        )


class NamedMatcher(Matcher):
    """Wrap a matcher with a custom description for nice stringification."""

    def __init__(self, description, matcher):
        super().__init__(description, matcher.__eq__)

    def __repr__(self):
        return self._description
