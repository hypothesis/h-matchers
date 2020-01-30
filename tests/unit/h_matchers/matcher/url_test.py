import pytest

from h_matchers import Any
from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.url import AnyURL

# We do lots of goofy comparisons on purpose
# pylint: disable=misplaced-comparison-constant,compare-to-empty-string


class TestAnyUrl:
    BASE_URL = "http://www.example.com/path?a=1&b=2#fragment"
    DIFFERENT_URLS = {
        "scheme": "CHANGE://www.example.com/path?a=1&b=2#fragment",
        "host": "http://CHANGE/path?a=1&b=2#fragment",
        "path": "http://www.example.com/CHANGE?a=1&b=2#fragment",
        "query": "http://www.example.com/path?CHANGE=1#fragment",
        "fragment": "http://www.example.com/path?a=1&b=2#CHANGE",
    }

    def test_base_case(self):
        matcher = AnyURL()

        assert "" == matcher
        assert None != matcher

    def test_base_url_requires_scheme(self):
        with pytest.raises(ValueError):
            AnyURL("no_scheme")

    @pytest.mark.parametrize("part,matching_url", tuple(DIFFERENT_URLS.items()))
    def test_base_matching_with_overwrite(self, part, matching_url):
        matcher = AnyURL(self.BASE_URL, **{part: Any()})

        assert self.BASE_URL == matcher
        assert matching_url == matcher

        for non_matching_part, non_matching_url in self.DIFFERENT_URLS.items():
            if non_matching_part == part:
                continue

            assert non_matching_url != matcher

    def test_case_sensitivity_for_other(self):
        matcher = AnyURL(self.BASE_URL)

        # https://tools.ietf.org/html/rfc7230#section-2.7.3
        # scheme and host are case-insensitive
        assert matcher == "HTTP://www.example.com/path?a=1&b=2#fragment"
        assert matcher == "http://WWW.EXAMPLE.COM/path?a=1&b=2#fragment"

        # ... all others not
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

        # ... all others not
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

        for comparison_part, url in self.DIFFERENT_URLS.items():
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
