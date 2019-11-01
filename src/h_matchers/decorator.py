"""Decorators for h-matchers."""


# Pylint doesn't understand this is a decorator
class fluent_entrypoint:  # pylint: disable=invalid-name
    """Makes a class method act as both a method and a classmethod.

    If the wrapped method is called as a classmethod an instance will first
    be created and then passed to the object. It is therefore important
    that you class not accept any arguments for instantiation.
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

    def __call__(self, *args, **kwargs):  # noqa: D102
        return self.function(self.instance, *args, **kwargs)
