"""
The core libraries for matching. These are not intended to be used directly.
"""
# pylint: disable=too-few-public-methods


class Matcher:
    """
    An abstract class for the matcher testing pattern whereby an object
    stands in for another and will evaluate to true when compared with the
    other.
    """

    def __init__(self, description, test_function):
        self._description = description
        self._test_function = test_function

    def __eq__(self, other):
        return self._test_function(other)

    def __str__(self):
        return self._description  # pragma: no cover

    def __repr__(self):
        return f"<{self.__class__.__name__} '{str(self)}'>"  # pragma: no cover
