import re

import pytest
from tests.unit.data_types import DataTypes

from h_matchers.string import AnyString, AnyStringContaining, AnyStringMatching


class TestAnyString:
    @pytest.mark.parametrize(
        "item,description", DataTypes.parameters(exact=DataTypes.Groups.STRINGS)
    )
    def test_it_matches(self, item, description):
        assert AnyString() == item
        assert item == AnyString()

    @pytest.mark.parametrize(
        "item,description", DataTypes.parameters(exclude=DataTypes.Groups.STRINGS)
    )
    def test_it_does_not_match(self, item, description):
        assert AnyString() != item
        assert item != AnyString()


class TestAnyStringContaining:
    def test_it_matches(self):
        matcher = AnyStringContaining("specific string")
        assert matcher == "a long string with a specific string in it"
        assert "a long string with a specific string in it" == matcher

    @pytest.mark.parametrize("item,description", DataTypes.parameters())
    def test_it_does_not_match(self, item, description):
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

    @pytest.mark.parametrize("item,description", DataTypes.parameters())
    def test_it_does_not_match(self, item, description):
        matcher = AnyStringMatching("a.*b")
        assert matcher != item
        assert item != matcher
