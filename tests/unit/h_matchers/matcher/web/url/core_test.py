import pytest

from h_matchers import Any
from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.web.url.core import AnyURLCore, MultiValueQuery

# We do lots of goofy comparisons on purpose
# pylint: disable=compare-to-empty-string


class TestAnyURL:
    def test_base_case(self):
        matcher = AnyURLCore()

        assert "" == matcher
        assert 3 != matcher

    BASE_URL = "http://www.example.com/path;params?a=1&b=2#fragment"

    # URLs where the specified part is different from BASE_URL
    PART_MODIFIED_URLS = {
        # We must use a URL scheme with `params` for this test
        "scheme": "ftp://www.example.com/path;params?a=1&b=2#fragment",
        "host": "http://MODIFIED/path;params?a=1&b=2#fragment",
        "path": "http://www.example.com/MODIFIED;params?a=1&b=2#fragment",
        "params": "http://www.example.com/path;MODIFIED?a=1&b=2#fragment",
        "query": "http://www.example.com/path;params?MODIFIED=1#fragment",
        "fragment": "http://www.example.com/path;params?a=1&b=2#MODIFIED",
    }

    @pytest.mark.parametrize(
        "part,url_with_part_changed", tuple(PART_MODIFIED_URLS.items())
    )
    def test_you_can_make_one_part_wild_with_a_base_url(
        self, part, url_with_part_changed
    ):
        # Create a matcher with the specified part wild i.e. `scheme=Any()`

        matcher = AnyURLCore(self.BASE_URL, **{part: Any()})

        # Check it matches the original URL and the URL with that part changed
        assert self.BASE_URL == matcher
        assert url_with_part_changed == matcher

    @pytest.mark.parametrize(
        "base_url, url",
        (
            ("http://example.com", "http://example.com"),
            ("http://example.com", "http://example.com/"),
            ("http://example.com/", "http://example.com"),
            ("http://example.com/", "http://example.com/"),
        ),
    )
    def test_base_url_matches_with_or_without_path(self, base_url, url):
        matcher = AnyURLCore(base_url=base_url)

        assert matcher == url

    @pytest.mark.parametrize("part", ["scheme", "host", "path", "query", "fragment"])
    def test_a_wild_part_does_not_just_match_everything(self, part):
        # Create a matcher with the specified part wild i.e. `scheme=Any()`
        matcher = AnyURLCore(self.BASE_URL, **{part: Any()})

        for modified_part, modified_url in self.PART_MODIFIED_URLS.items():
            # We expect to match the part where the modified part is the part
            # we have made wild so skip
            if modified_part == part:
                continue

            assert modified_url != matcher

    @pytest.mark.parametrize(
        "part,url_with_part_missing",
        (
            # URLs where the specified part is missing from BASE_URL
            ("scheme", "www.example.com/path;params?a=1&b=2#fragment"),
            ("host", "http:///path;params?a=1&b=2#fragment"),
            ("path", "http://www.example.com;params?a=1&b=2#fragment"),
            ("params", "http://www.example.com/path?a=1&b=2#fragment"),
            ("query", "http://www.example.com/path;params#fragment"),
            ("fragment", "http://www.example.com/path;params?a=1&b=2"),
        ),
    )
    def test_you_can_override_default_with_params(self, part, url_with_part_missing):
        # Create a matcher with the specified part set to None
        # i.e. `scheme=None`
        matcher = AnyURLCore(**{part: None})

        # Check we match the URL with the part missing
        assert url_with_part_missing == matcher
        # ... but not the URL with it present
        assert self.BASE_URL != matcher

    def test_case_sensitivity_for_other(self):
        matcher = AnyURLCore(self.BASE_URL)

        # https://tools.ietf.org/html/rfc7230#section-2.7.3
        # scheme and host are case-insensitive
        assert matcher == "HTTP://www.example.com/path;params?a=1&b=2#fragment"
        assert matcher == "http://WWW.EXAMPLE.COM/path;params?a=1&b=2#fragment"

        # ... path, query string and fragment are case-sensitive
        assert matcher != "http://www.example.com/PATH;params?a=1&b=2#fragment"
        assert matcher != "http://www.example.com/path;PARAMS?a=1&b=2#fragment"
        assert matcher != "http://www.example.com/path;params?A=1&B=2#fragment"
        assert matcher != "http://www.example.com/path;params?a=1&b=2#FRAGMENT"

    @pytest.mark.parametrize(
        "matcher",
        (
            AnyURLCore(BASE_URL.upper()),
            AnyURLCore(BASE_URL.upper(), scheme="HTTP"),
            AnyURLCore(BASE_URL.upper(), host="WWW.EXAMPLE.COM"),
        ),
    )
    def test_case_sensitivity_for_self(self, matcher):
        # https://tools.ietf.org/html/rfc7230#section-2.7.3
        # scheme and host are case-insensitive
        assert matcher == "http://WWW.EXAMPLE.COM/PATH;PARAMS?A=1&B=2#FRAGMENT"
        assert matcher == "HTTP://www.example.com/PATH;PARAMS?A=1&B=2#FRAGMENT"

        # ... path, query string and fragment are case-sensitive
        assert matcher != "HTTP://WWW.EXAMPLE.COM/path;PARAMS?A=1&B=2#FRAGMENT"
        assert matcher != "HTTP://WWW.EXAMPLE.COM/PATH;params?A=1&B=2#FRAGMENT"
        assert matcher != "HTTP://WWW.EXAMPLE.COM/PATH;PARAMS?a=1&b=2#FRAGMENT"
        assert matcher != "HTTP://WWW.EXAMPLE.COM/PATH;PARAMS?A=1&B=2#fragment"

    @pytest.mark.parametrize(
        "part,value",
        (
            ("scheme", "http"),
            ("host", "www.example.com"),
            ("path", "/path"),
            ("query", "a=1&b=2"),
            ("fragment", "fragment"),
        ),
    )
    def test_generic_matching(self, part, value):
        matcher = AnyURLCore(**{part: value})

        for comparison_part, url in self.PART_MODIFIED_URLS.items():
            if comparison_part == part:
                # The URLs are different here and this is the part we specified
                # so we should spot the difference
                assert url != matcher
            else:
                # These are different too, but these should all match
                assert url == matcher

    @pytest.mark.parametrize(
        "_,query",
        (
            ("plain string", "a=1&b=2"),
            ("dict", {"a": "1", "b": "2"}),
            ("any mapping", AnyMapping.containing({"a": "1", "b": "2"}).only()),
            ("any dict", Any.dict.containing({"a": "1", "b": "2"}).only()),
        ),
    )
    def test_specifying_query_string(self, query, _):
        matcher = AnyURLCore(query=query)

        assert matcher == "http://example.com?b=2&a=1"

        assert matcher != "http://example.com?b=2"
        assert matcher != "http://example.com?b=2&a=1&c=3"
        assert matcher != "http://example.com?b=2&a=1&a=1"

    def test_multi_query_params(self):
        url = "http://example.com?a=1&a=1&a=2"

        assert url != AnyURLCore(query={"a": "1"})
        assert url != AnyURLCore(query=Any.dict.containing({"a": "1"}))
        assert url == AnyURLCore(query=Any.mapping.containing({"a": "1"}))

        assert url == AnyURLCore(
            query=Any.mapping.containing([("a", "1"), ("a", "2"), ("a", "1")]).only()
        )
        assert url != AnyURLCore(
            query=Any.mapping.containing(
                [("a", "1"), ("a", "2"), ("a", "1"), ("b", 5)]
            ).only()
        )

    def test_stringification_changes_when_contents_change(self):
        matcher = AnyURLCore(scheme="foo")

        assert "foo" in repr(matcher)
        assert "foo" in str(matcher)

        matcher.parts["scheme"] = "boo"

        assert "boo" in repr(matcher)
        assert "boo" in str(matcher)

    def test_it_raises_with_assert_on_comparison_enabled(self):
        # Normally you'd turn this on for the whole class, but it has totally
        # non-local effects and explodes the tests
        matcher = AnyURLCore(scheme="missing")
        matcher.assert_on_comparison = True

        with pytest.raises(AssertionError):
            _ = "abc" == matcher

    @pytest.mark.parametrize("other", (None, 123, True))
    def test_it_refuses_to_compare_to_non_strings(self, other):
        assert AnyURLCore() != other

    def test_stringification_default(self):
        assert str(AnyURLCore()) == "* any URL *"


class TestAnyURLPathMatching:
    def test_we_match_full_paths_with_or_without_slashes(self):
        assert "http://example.com/path" == AnyURLCore(path="path")
        assert "http://example.com/path" == AnyURLCore(path="/path")

    def test_if_you_specify_slash_in_the_path_its_mandatory(self):
        matcher = AnyURLCore(path="/path")

        assert "path" != matcher
        assert "/path" == matcher

    def test_if_you_dont_specify_slash_in_the_path_its_optional(self):
        matcher = AnyURLCore(path="path")

        assert "path" == matcher
        assert "/path" == matcher

    def test_if_you_have_no_scheme_the_path_is_exact(self):
        matcher = AnyURLCore(scheme=None, host=None, path="path")

        assert "path" == matcher
        assert "/path" != matcher

        matcher = AnyURLCore(scheme=None, host=None, path="/path")

        assert "path" != matcher
        assert "/path" == matcher

    def test_it_does_not_match_prefixes_alone(self):
        assert AnyURLCore(path="/start") != "http://example.com/start/more"


class TestAnyURLHostnameGuessing:
    @pytest.mark.parametrize(
        "url,expected_host,expected_path",
        (
            # A bare path without a leading / is the only time we have no
            # leading slash
            ("path", None, "path"),
            ("examplecom/path", None, "examplecom/path"),
            # All other paths should have one if they exist
            ("/path", None, "/path"),
            ("example.com/", "example.com", "/"),
            ("example.com/path", "example.com", "/path"),
            ("/example.com/path", None, "/example.com/path"),
            ("127.0.0.1/path", "127.0.0.1", "/path"),
            # Indicators of bare hostnames should be respected
            ("localhost", "localhost", None),
            ("example.com", "example.com", None),
            # A scheme tells us the next part is a host
            ("http://example.com/", "example.com", "/"),
            ("http://path", "path", None),
            ("http:///path", None, "/path"),
            ("http://?a=b", None, None),
            # Skip
            # These get interpreted inconsistently as scheme / path
            # ("localhost:9000", "localhost:9000", None),
            # ("localhost:9000/path", "localhost:9000", "/path"),
        ),
    )
    def test_hostname_guessing(self, url, expected_host, expected_path):
        parsed = AnyURLCore.parse_url(url)
        assert (parsed["host"], parsed["path"]) == (expected_host, expected_path)


class TestMultiValueQuery:
    def test_it_stringifies(self):
        query = MultiValueQuery(["1234"])
        assert "MultiValueQuery" in repr(query)
        assert "1234" in repr(query)
