"""Flexible matchers for various collection types in a fluent style."""

from h_matchers.exception import NoMatch
from h_matchers.matcher.collection import _mixin
from h_matchers.matcher.core import Matcher


class AnyCollection(
    _mixin.SizeMixin,
    _mixin.TypeMixin,
    _mixin.ItemMatcherMixin,
    _mixin.ContainsMixin,
    Matcher,
):
    """Matches any iterable with options for constraining contents and size."""

    def __init__(self):
        # Pass None as our function, as we will be in charge of our own type
        # checking
        super().__init__("dummy", None)

    def __eq__(self, other):
        try:
            copy = list(other)
        except TypeError:
            # Not iterable
            return False

        # Execute checks roughly in complexity order
        for checker in [
            self._check_type,
            self._check_size,
            self._check_item_matcher,
            self._check_contains,
        ]:
            try:
                checker(copy, original=other)
            except NoMatch:
                return False

        return True

    def __str__(self):
        # This is some pretty gross code, but it makes test output so much
        # more readable
        parts = ["any"]

        parts.extend(self._describe_type())
        parts.extend(self._describe_size())
        parts.extend(self._describe_contains())
        parts.extend(self._describe_item_matcher())

        return f'* {" ".join(parts)} *'


class AnyDict(AnyCollection):
    """A matcher representing any dict."""

    _exact_type = dict


class AnySet(AnyCollection):
    """A matcher representing any set."""

    _exact_type = set


class AnyList(AnyCollection):
    """A matcher representing any list."""

    _exact_type = list


class AnyMapping(AnyCollection):
    """A matcher representing any mapping."""

    def __eq__(self, other):
        if not hasattr(other, "items"):
            return False

        return super().__eq__(other)
