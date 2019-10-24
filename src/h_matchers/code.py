"""
Classes implementing the matcher pattern for comparing to
functions and classes etc.
"""
# pylint: disable=too-few-public-methods

from h_matchers.core import LambdaMatcher


class AnyInstanceOfClass(LambdaMatcher):
    """A class that matches any instance of another class"""

    def __init__(self, klass):
        super().__init__(klass.__name__, lambda other: isinstance(other, klass))


class AnyFunction(LambdaMatcher):
    """A class that matches any callable object"""

    def __init__(self):
        super().__init__("* any callable *", callable)
