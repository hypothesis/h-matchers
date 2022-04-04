import re

import pytest

from h_matchers.matcher.strings import AnyString, AnyStringContaining, AnyStringMatching
from tests.unit.data_types import DataTypes


class TestAnyString:
    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exact=DataTypes.Groups.STRINGS)
    )
    def test_it_matches(self, item, _):
        assert AnyString() == item
        assert item == AnyString()

    @pytest.mark.parametrize(
        "item,_", DataTypes.parameters(exclude=DataTypes.Groups.STRINGS)
    )
    def test_it_does_not_match(self, item, _):
        assert AnyString() != item
        assert item != AnyString()

    @pytest.mark.parametrize("attribute", ["containing", "matching"])
    def test_it_has_expected_attributes(self, attribute):
        assert hasattr(AnyString, attribute)


class TestAnyStringContaining:
    def test_it_matches(self):
        matcher = AnyStringContaining("specific string")
        assert matcher == "a long string with a specific string in it"

        assert "a long string with a specific string in it" == matcher

    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_does_not_match(self, item, _):
        matcher = AnyStringContaining("specific string")
        assert matcher != item
        assert item != matcher


class TestAnyStringMatching:
    def test_it_matches(self):
        matcher = AnyStringMatching("a.*b")
        assert matcher == "a to b"

        assert "a to b" == matcher
        assert "A to B" != matcher

    def test_it_matches_with_flags(self):
        matcher = AnyStringMatching("a.*b", flags=re.IGNORECASE)
        assert matcher == "a to b"

        assert "A to B" == matcher

    @pytest.mark.parametrize("item,_", DataTypes.parameters())
    def test_it_does_not_match(self, item, _):
        matcher = AnyStringMatching("a.*b")
        assert matcher != item
        assert item != matcher
