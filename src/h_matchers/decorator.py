"""
Decorators for h-matchers
"""


# Pylint doesn't understand this is a decorator
class fluent_entrypoint:  # pylint: disable=invalid-name
    """
    A decorator allowing a method on a class to act as either an instance
    method, or a class method (which will first create a blank instance of the
    class).
    """

    instance = None

    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        # If we have been called in a classmethod context, create a new
        # instance of the owning object
        if instance is None:
            instance = owner()
        self.instance = instance

        return self.__call__

    def __call__(self, *args, **kwargs):
        return self.function(self.instance, *args, **kwargs)
