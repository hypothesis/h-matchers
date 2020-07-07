"""A mixin for AnyCollection which lets you specify the size."""

# pylint: disable=too-few-public-methods

from h_matchers.decorator import fluent_entrypoint
from h_matchers.exception import NoMatch


class SizeMixin:
    """Apply and check size constraints."""

    _min_size = None
    _max_size = None

    @staticmethod
    def of_size(exact=None, at_least=None, at_most=None):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    # pylint: disable=function-redefined
    def of_size(self, exact=None, at_least=None, at_most=None):
        """Limit the size of the list.

        Can be called as an instance or class method.

        :param exact: Specify an exact size
        :param at_least: Specify a minimum size
        :param at_most: Specify a maximum size
        :raises ValueError: If arguments are missing or incompatible
        """
        if exact is not None:
            self._min_size = exact
            self._max_size = exact

        elif at_least is None and at_most is None:
            raise ValueError("At least one option should not be None")

        else:
            if at_least is not None and at_most is not None and at_least > at_most:
                raise ValueError("The upper bound must be higher than the lower bound")

            self._min_size = at_least
            self._max_size = at_most

    # pylint: disable=unused-argument
    def _check_size(self, other, original=None):
        """Run the size check (if any)."""
        if self._min_size and len(other) < self._min_size:
            raise NoMatch("Too small")

        if self._max_size and len(other) > self._max_size:
            raise NoMatch("Too big")

    def _describe_size(self):
        if self._min_size is None and self._max_size is None:
            return

        if self._min_size == self._max_size:
            yield f"of length {self._min_size}"
        elif self._min_size is not None and self._max_size is not None:
            yield f"with length between {self._min_size} and {self._max_size}"

        elif self._min_size is not None:
            yield f"with length > {self._min_size}"
        else:
            yield f"with length < {self._max_size}"
