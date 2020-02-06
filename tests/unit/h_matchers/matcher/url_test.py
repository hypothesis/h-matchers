import pytest

from h_matchers import Any
from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.url import AnyURL, MultiValueQuery

# We do lots of goofy comparisons on purpose
# pylint: disable=misplaced-comparison-constant,compare-to-empty-string


class TestAnyUrl:
    BASE_URL = "http://www.example.com/path?a=1&b=2#fragment"

    # URLs where the specified part is different from BASE_URL
    PART_MODIFIED_URLS = {
        "scheme": "MODIFIED://www.example.com/path?a=1&b=2#fragment",
        "host": "http://MODIFIED/path?a=1&b=2#fragment",
        "path": "http://www.example.com/MODIFIED?a=1&b=2#fragment",
        "query": "http://www.example.com/path?MODIFIED=1#fragment",
        "fragment": "http://www.example.com/path?a=1&b=2#MODIFIED",
    }

    # URLs where the specified part is missing from BASE_URL
    PART_MISSING_URLS = {
        "scheme": "www.example.com/path?a=1&b=2#fragment",
        "host": "http:///path?a=1&b=2#fragment",
        "path": "http://www.example.com?a=1&b=2#fragment",
        "query": "http://www.example.com/path#fragment",
        "fragment": "http://www.example.com/path?a=1&b=2",
    }

    def test_base_case(self):
        matcher = AnyURL()

        assert "" == matcher
        assert None != matcher

    @pytest.mark.parametrize("part,matching_url", tuple(PART_MODIFIED_URLS.items()))
    def test_you_can_override_base_matching_with_params(self, part, matching_url):
        matcher = AnyURL(self.BASE_URL, **{part: Any()})

        assert self.BASE_URL == matcher
        assert matching_url == matcher

        # Check we don't accidentally match a URL where another part is
        # different
        for modified_part, modified_url in self.PART_MODIFIED_URLS.items():
            if modified_part == part:
                continue

            assert modified_url != matcher

    @pytest.mark.parametrize("part,matching_url", tuple(PART_MISSING_URLS.items()))
    def test_you_can_override_default_with_params(self, part, matching_url):
        # When setting one part to None, that part is definitely set to None
        # and not left as the default matcher instance
        matcher = AnyURL(**{part: None})

        # A little whitebox testing never killed anyone
        assert matcher.parts[part] is None

        print(AnyURL.parse_url(matching_url))
        assert matching_url == matcher
        assert matching_url != self.BASE_URL

    def test_case_sensitivity_for_other(self):
        matcher = AnyURL(self.BASE_URL)

        # https://tools.ietf.org/html/rfc7230#section-2.7.3
        # scheme and host are case-insensitive
        assert matcher == "HTTP://www.example.com/path?a=1&b=2#fragment"
        assert matcher == "http://WWW.EXAMPLE.COM/path?a=1&b=2#fragment"

        # ... path, query string and fragment are case-sensitive
        assert matcher != "http://www.example.com/PATH?a=1&b=2#fragment"
        assert matcher != "http://www.example.com/path?A=1&B=2#fragment"
        assert matcher != "http://www.example.com/path?a=1&b=2#FRAGMENT"

    @pytest.mark.parametrize(
        "matcher",
        (
            AnyURL(BASE_URL.upper()),
            AnyURL(BASE_URL.upper(), scheme="HTTP"),
            AnyURL(BASE_URL.upper(), host="WWW.EXAMPLE.COM"),
        ),
    )
    def test_case_sensitivity_for_self(self, matcher):
        # https://tools.ietf.org/html/rfc7230#section-2.7.3
        # scheme and host are case-insensitive
        assert matcher == "http://WWW.EXAMPLE.COM/PATH?A=1&B=2#FRAGMENT"
        assert matcher == "HTTP://www.example.com/PATH?A=1&B=2#FRAGMENT"

        # ... path, query string and fragment are case-sensitive
        assert matcher != "HTTP://WWW.EXAMPLE.COM/path?A=1&B=2#FRAGMENT"
        assert matcher != "HTTP://WWW.EXAMPLE.COM/PATH?a=1&b=2#FRAGMENT"
        assert matcher != "HTTP://WWW.EXAMPLE.COM/PATH?A=1&B=2#fragment"

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
        matcher = AnyURL(**{part: value})

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
        matcher = AnyURL(query=query)

        assert matcher == "http://example.com?b=2&a=1"

        assert matcher != "http://example.com?b=2"
        assert matcher != "http://example.com?b=2&a=1&c=3"
        assert matcher != "http://example.com?b=2&a=1&a=1"

    def test_multi_query_params(self):
        url = "http://example.com?a=1&a=1&a=2"

        assert url != AnyURL(query={"a": "1"})
        assert url != AnyURL(query=Any.dict.containing({"a": "1"}))
        assert url == AnyURL(query=Any.mapping.containing({"a": "1"}))

        assert url == AnyURL(
            query=Any.mapping.containing([("a", "1"), ("a", "2"), ("a", "1")]).only()
        )
        assert url != AnyURL(
            query=Any.mapping.containing(
                [("a", "1"), ("a", "2"), ("a", "1"), ("b", 5)]
            ).only()
        )

    @pytest.mark.parametrize(
        "url,expected_host,expected_path",
        (
            ("/path", None, "/path"),
            ("path", None, "path"),
            ("localhost", "localhost", None),
            ("localhost:9000", "localhost:9000", None),
            ("example.com", "example.com", None),
            ("example.com/path", "example.com", "path"),
            ("/example.com/path", None, "/example.com/path"),
            ("examplecom/path", None, "examplecom/path"),
            ("127.0.0.1/path", "127.0.0.1", "path"),
            # A scheme tells us the next part is a host
            ("http://path", "path", None),
            ("http:///path", None, "/path"),
            ("http://?a=b", None, None),
        ),
    )
    def test_hostname_guessing(self, url, expected_host, expected_path):
        parsed = AnyURL.parse_url(url)
        assert (parsed["host"], parsed["path"]) == (expected_host, expected_path)


class TestMultiValueQuery:
    def test_it_stringifies(self):
        query = MultiValueQuery(["1234"])
        assert "MultiValueQuery" in repr(query)
        assert "1234" in repr(query)
