import pytest

from h_matchers.exception import NoMatch
from h_matchers.matcher.collection._mixin.size import SizeMixin


class HostClass(SizeMixin):
    def __eq__(self, other):
        try:
            self._check_size(list(other))

        except NoMatch:
            return False

        return True


class TestSizeMixin:
    def test_it_matches_exact_size(self):
        matcher = HostClass.of_size(3)

        assert matcher == [1, 2, 3]
        assert {1, 2, 3} == matcher
        assert matcher != set()
        assert matcher != [1, 2]

    def test_it_matches_minimum_size(self):
        matcher = HostClass.of_size(at_least=2)

        assert matcher == [1, 2]
        assert matcher == [1, 2, 3]
        assert matcher != [1]

    def test_it_complains_with_incorrect_size(self):
        with pytest.raises(ValueError):
            HostClass.of_size()

        with pytest.raises(ValueError):
            HostClass.of_size(at_least=100, at_most=1)

    def test_it_matches_maximum_size(self):
        matcher = HostClass.of_size(at_most=2)

        # pylint:disable=use-implicit-booleaness-not-comparison
        assert matcher == []
        assert matcher == [1, 2]
        assert matcher != [1, 2, 3]
