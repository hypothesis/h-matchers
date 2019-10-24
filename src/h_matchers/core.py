# pylint: disable=too-few-public-methods


class Matcher:
    """
    An abstract class for the matcher testing pattern whereby an object
    stands in for another and will evaluate to true when compared with the
    other.
    """

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description  # pragma: no cover

    def __repr__(self):
        return f"<{self.__class__.__name__} '{str(self)}'>"  # pragma: no cover


class LambdaMatcher(Matcher):
    """
    Implements the matcher pattern when given a test function which tests if we
    are equal to another object.
    """

    def __init__(self, description, test_function):
        super().__init__(description)
        self.test_function = test_function

    def __eq__(self, other):
        return self.test_function(other)
