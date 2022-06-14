from unittest.mock import create_autospec, sentinel

import pytest

from h_matchers.matcher.core import Matcher


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

    def test_it_compares_as_not_equal_for_AssertionError(self, raise_assertion_error):
        assert Matcher(sentinel.description, raise_assertion_error) != sentinel.other
        raise_assertion_error.assert_called_once_with(sentinel.other)

    def test_it_compares_at_not_equal_if_assert_on_comparison(
        self, raise_assertion_error
    ):
        matcher = Matcher(sentinel.description, raise_assertion_error)
        matcher.assert_on_comparison = True

        with pytest.raises(AssertionError):
            # pylint: disable=pointless-statement
            matcher == sentinel.other

    def test_it_grabs_last_matched(self, function):
        function.side_effect = (True, False)
        matcher = Matcher(sentinel.description, function)

        assert matcher.last_matched(None) is None
        assert matcher.last_matched(...) is ...
        assert not matcher.matched_to

        assert matcher == "match"
        assert matcher != "not_match"

        assert matcher.last_matched() == "match"
        assert matcher.matched_to == ["match"]

    @pytest.fixture
    def raise_assertion_error(self, function):
        function.side_effect = AssertionError
        return function

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
