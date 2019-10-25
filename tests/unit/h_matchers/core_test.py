from unittest.mock import create_autospec, sentinel

import pytest

from h_matchers.core import Matcher


class TestMatcher:
    def test_it_stringifies(self, function):
        assert str(Matcher("abcde", function)) == "abcde"

    def test_it_creates_a_nice_repr(self, function):
        class MyChild(Matcher):
            pass

        description = repr(MyChild("abcde", function))

        assert "abcde" in description
        assert "MyChild" in description

    def test_it_compares_as_equal_when_function_returns_True(self, true_dat):
        assert Matcher(sentinel.description, true_dat) == sentinel.other
        true_dat.assert_called_once_with(sentinel.other)

    def test_it_compares_as_not_equal_when_function_returns_False(self, no_way):
        assert Matcher(sentinel.description, no_way) != sentinel.other
        no_way.assert_called_once_with(sentinel.other)

    @pytest.fixture
    def true_dat(self, function):
        function.return_value = True
        return function

    @pytest.fixture
    def no_way(self, function):
        function.return_value = False
        return function

    @pytest.fixture
    def function(self):
        function = create_autospec(lambda other: True)  # pragma: no cover

        return function
