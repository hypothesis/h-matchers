"""The core classes for matching.

These are not intended to be used directly.
"""


class Matcher:
    """Used as the base class for concrete matching classes.

    Implements a base class for use in the testing pattern where an object
    stands in for another and will evaluate to true when compared with the
    other.
    """

    assert_on_comparison = False
    """
    Enable raising on comparison instead of returning False.

    This can be very useful for debugging as we can fail fast and return a
    message about why we can't match. We might want to think about making this
    a more general feature. It is up to individual matchers to support it.
    """

    matched_to: list
    """A list of all matched objects."""

    def __init__(self, description, test_function):
        self._description = description
        self._test_function = test_function
        self.reset()

    def __eq__(self, other):
        try:
            matches = self._test_function(other)
        except AssertionError:
            if self.assert_on_comparison:
                raise
            matches = False

        if matches:
            self.matched_to.append(other)

        return matches

    def last_matched(self, default=None):
        """Get the last matched object, if any.

        :param default: Default to return on no match. This can be used to
            distinguish between not matching and matching None.
        """
        return self.matched_to[-1] if self.matched_to else default

    def reset(self):
        """Clear any stored data (like `last_matched`)."""

        self.matched_to = []

    def __str__(self):
        return self._description  # pragma: no cover

    def __repr__(self):
        return f"<{self.__class__.__name__} '{str(self)}'>"  # pragma: no cover
