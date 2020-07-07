"""Decorators for h-matchers."""


# Pylint doesn't understand this is a decorator
class fluent_entrypoint:  # pylint: disable=invalid-name,too-few-public-methods
    """Makes a class method act as both a method and a classmethod.

    If the wrapped method is called as a classmethod an instance will first
    be created and then passed to the object. It is therefore important
    that you class not accept any arguments for instantiation.

    This will automatically return `self` for fluent chaining in your methods.
    """

    def __init__(self, function):
        self.function = function

    def __get__(self, obj, _type=None):
        # If we have been called in a classmethod context, create a new
        # instance of the owning object
        if obj is None:
            obj = _type()

        def wrapper(*args, **kwargs):
            self.function(obj, *args, **kwargs)

            return obj

        return wrapper
