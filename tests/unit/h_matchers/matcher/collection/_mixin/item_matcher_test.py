from h_matchers import Any
from h_matchers.exception import NoMatch
from h_matchers.matcher.collection._mixin.item_matcher import ItemMatcherMixin


class HostClass(ItemMatcherMixin):
    def __eq__(self, other):
        try:
            self._check_item_matcher(list(other), None)

        except NoMatch:
            return False

        return True


class TestItemMatcherMixin:
    def test_it_can_apply_a_matcher_to_all_elements(self):
        matcher = HostClass.comprised_of(Any.string())

        assert matcher == ["a", "b"]
        assert matcher == {"a": 1, "b": 2}

        assert matcher != ["a", "b", 1]
        assert matcher != {"a": 1, "b": 1, 3: None}

    def test_it_can_match_objects_with_equals(self):
        class NeverMatches:
            def __eq__(self, other):  # pragma: no cover
                return False

        matcher = HostClass.comprised_of(Any.instance_of(NeverMatches))

        assert matcher == [NeverMatches()]
