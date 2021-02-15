import pytest

from h_matchers.matcher.anything import AnyThing
from h_matchers.matcher.web.url.fluent import AnyURL

# pylint: disable=compare-to-empty-string


class TestAnyURLFluent:
    def test_basic_setup(self):
        pass

    def test_matching_base_url(self):
        url = "http://example.com"
        matcher = AnyURL.matching(url)

        assert matcher == url
        assert matcher != (url + "?a=b")

    def test_with_scheme_required(self):
        matcher = AnyURL.with_scheme()

        assert matcher == "http://"
        assert matcher != "www.example.com"

    def test_with_scheme_specified(self):
        matcher = AnyURL.with_scheme("http")
        assert matcher == "http://"
        assert matcher != "https://"

    def test_with_host_required(self):
        matcher = AnyURL.with_host()

        assert matcher == "www.example.com"
        assert matcher != "http://"

    def test_with_host_specified(self):
        matcher = AnyURL.with_host("www.example.com")

        assert matcher == "http://www.example.com"
        assert matcher != "http://ftp.example.com"

    def test_with_path_required(self):
        matcher = AnyURL.with_path()

        assert matcher == "/path"
        assert matcher != "http://example.com"

    def test_with_path_specified(self):
        matcher = AnyURL.with_path("path")

        assert matcher == "http://example.com/path"
        assert matcher != "http://example.com/different_path"
        assert matcher != "http://example.com/"

    def test_with_params_required(self):
        matcher = AnyURL.with_params()

        assert matcher == "http://example.com/path;params"
        assert matcher != "http://example.com/path"

    def test_with_params_specified(self):
        matcher = AnyURL.with_params("params")

        assert matcher == "http://www.example.com/path;params"
        assert matcher != "http://www.example.com/path;different"

    def test_containing_query(self):
        matcher = AnyURL.containing_query({"a": "b"})

        assert matcher == "?a=b"
        assert matcher == "?a=b&a=c"
        assert matcher == "?a=c&a=b"

        assert matcher != ""
        assert matcher != "?e=f"

    def test_with_query_required(self):
        matcher = AnyURL.with_query()

        assert matcher == "?a=b"
        assert matcher != ""

    def test_with_query_specified(self):
        matcher = AnyURL.with_query({"a": "b"})

        assert matcher == "?a=b"
        assert matcher != "?a=b&a=c"
        assert matcher != ""

    def test_with_fragment_required(self):
        matcher = AnyURL.with_fragment()

        assert matcher == "#fragment"
        assert matcher == "http://example.com#fragment"
        assert matcher == "#different"
        assert matcher != "http://example.com"

    def test_with_fragment_specified(self):
        matcher = AnyURL.with_fragment("fragment")

        assert matcher == "#fragment"
        assert matcher == "http://example.com#fragment"
        assert matcher != "#different"
        assert matcher != "http://example.com"

    @pytest.mark.parametrize(
        "method,part",
        (
            (AnyURL.with_scheme, "scheme"),
            (AnyURL.with_host, "host"),
            (AnyURL.with_path, "path"),
            (AnyURL.with_query, "query"),
            (AnyURL.containing_query, "query"),
            (AnyURL.with_fragment, "fragment"),
        ),
    )
    def test_we_can_set_any_matcher(self, method, part):
        any_matcher = AnyThing()
        matcher = method(any_matcher)

        assert matcher.parts[part] is any_matcher

    def test_all_methods_together(self):
        base_url = "http://example.com/path?a=b#fragment"
        matcher = (
            AnyURL.matching(base_url)
            .with_host("www.example.com")
            .with_path("/different")
            .with_query({"b": "a"})
            .with_fragment("new_fragment")
        )

        assert matcher != base_url
        assert matcher == "http://www.example.com/different?b=a#new_fragment"

        matcher = matcher.with_scheme("ftp").containing_query({"c": "d"})

        assert matcher == "ftp://www.example.com/different?b=a&c=d#new_fragment"
