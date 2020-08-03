"""The core classes for matching.

These are not intended to be used directly.
"""

# pylint: disable=too-few-public-methods


class Matcher:
    """Used as the base class for concrete matching classes.

    Implements a base class for use in the testing pattern where an object
    stands in for another and will evaluate to true when compared with the
    other.
    """

    # Enable raising on comparison instead of returning False. This can be very
    # useful for debugging as we can fail fast and return a message about why
    # we can't match. We might want to think about making this a more general
    # feature. It is up to individual matchers to support it
    assert_on_comparison = False

    def __init__(self, description, test_function):
        self._description = description
        self._test_function = test_function

    def __eq__(self, other):
        return self._test_function(other)

    def __str__(self):
        return self._description  # pragma: no cover

    def __repr__(self):
        return f"<{self.__class__.__name__} '{str(self)}'>"  # pragma: no cover
