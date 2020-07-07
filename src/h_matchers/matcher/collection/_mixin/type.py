"""A mixin for AnyCollection which lets you specify the type."""

# pylint: disable=too-few-public-methods

from h_matchers.decorator import fluent_entrypoint
from h_matchers.exception import NoMatch


class TypeMixin:
    """Apply and check type constraint."""

    _exact_type = None

    @staticmethod
    def of_type(of_type):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    # pylint: disable=function-redefined
    def of_type(self, of_type):
        """Limit the type to a specific type like `list` or `set`.

        Can be called as an instance or class method.
        """
        self._exact_type = of_type

    def _check_type(self, _, original):
        if self._exact_type:
            if not isinstance(original, self._exact_type):
                raise NoMatch("Wrong type")

    def _describe_type(self):
        if self._exact_type:
            yield self._exact_type.__name__
        else:
            yield "iterable"
