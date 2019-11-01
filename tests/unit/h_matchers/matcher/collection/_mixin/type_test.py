from h_matchers.exception import NoMatch
from h_matchers.matcher.collection._mixin.type import TypeMixin

# pylint: disable=no-value-for-parameter


class HostClass(TypeMixin):
    def __eq__(self, other):
        try:
            self._check_type(None, original=other)

        except NoMatch:
            return False

        return True


class TestTypeMixin:
    def test_it_matches_specific_class(self):
        matcher = HostClass.of_type(list)

        assert matcher == []
        assert [] == matcher
        assert matcher != set()
        assert set() != matcher