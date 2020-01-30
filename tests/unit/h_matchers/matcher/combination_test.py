from h_matchers.matcher.combination import AllOf, AnyOf
from h_matchers.matcher.string import AnyString

# pylint: disable=misplaced-comparison-constant,singleton-comparison


class TestAnyOf:
    def test_any_match_will_do(self):
        matcher = AnyOf([1, None, "fish"])

        assert None == matcher
        assert 1 == matcher
        assert "fish" == matcher

        assert 2 != matcher

    def test_it_can_use_generators(self):
        matcher = AnyOf(iter(range(3)))

        assert matcher == 2
        assert matcher == 2
        assert matcher != 10


class TestAllOf:
    def test_requires_all_things_to_match(self):
        matcher = AllOf(
            [AnyString(), AnyString.containing("foo"), AnyString.containing("bar"),]
        )

        assert matcher == "foo bar"
        assert matcher != "foo"
        assert matcher != "bar"

    def test_it_can_use_generators(self):
        matcher = AllOf(iter(range(1, 2)))

        assert matcher == 1
        assert matcher == 1
        assert matcher != 10