from urllib.parse import urlparse

import pytest
from pyramid.request import Request as PyramidRequest
from pyramid.testing import DummyRequest
from pytest import param
from requests import PreparedRequest, Request

from h_matchers import Any
from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.web.request import AnyRequest

# We have a lot of fixtures going on in this file
# pylint: disable=too-many-arguments,too-many-positional-arguments


class TestAnyRequest:
    @pytest.mark.parametrize(
        "request_method,matcher_method,matches",
        (
            ("POST", None, True),
            ("GET", None, True),
            ("POST", "POST", True),
            ("GET", "GET", True),
            ("PoSt", "pOsT", True),
            ("POST", "GET", False),
            ("POST", Any.string(), True),
            ("POST", Any.string.containing("OS"), True),
            ("GET", Any.string.containing("OS"), False),
        ),
    )
    def test_can_match_method(
        self, request_method, matcher_method, matches, make_request, is_fluent
    ):
        request = make_request(method=request_method)

        matcher = (
            AnyRequest.with_method(matcher_method)
            if is_fluent
            else AnyRequest(method=matcher_method)
        )

        assert (request == matcher) is matches

    @pytest.mark.parametrize(
        "request_url,matcher_url,matches",
        (
            ("http://example.com/", None, True),
            ("http://example.com/", "http://example.com", True),
            ("http://EXAMPLE.COM", "http://example.com/", True),
            ("http://example.com/path", "http://example.com/path", True),
            ("http://not.example.com/", "http://example.com/", False),
            ("http://example.com/", Any.url(host="example.com"), True),
            ("http://not.example.com/", Any.url(host="example.com"), False),
        ),
    )
    def test_can_match_url(
        self, request_url, matcher_url, matches, make_request, is_fluent
    ):
        request = make_request(url=request_url)

        matcher = (
            AnyRequest.with_url(matcher_url)
            if is_fluent
            else AnyRequest(url=matcher_url)
        )

        assert (request == matcher) is matches

    @pytest.mark.parametrize(
        "header_matcher,matches",
        (
            param({"A": "a", "B": "b", "C": "c"}, False, id="Super set"),
            param({"A": "a", "B": "b"}, True, id="Exact match"),
            param({"A": "a"}, False, id="Sub set"),
            param(AnyMapping(), True, id="Matcher"),
            (None, True),
        ),
    )
    def test_can_match_headers(self, make_request, header_matcher, matches, is_fluent):
        headers = {"A": "a", "B": "b"}
        request = make_request(headers=headers)

        if is_fluent:
            matcher = AnyRequest.with_headers(header_matcher)
        else:
            matcher = AnyRequest(headers=header_matcher)

        assert (request == matcher) is matches

    @pytest.mark.parametrize(
        "header_matcher,matches",
        (
            param({"A": "a", "B": "b", "C": "c"}, False, id="Super set"),
            param({"A": "a", "B": "b"}, True, id="Exact match"),
            param({"A": "a"}, True, id="Sub set"),
            param(AnyMapping(), True, id="Matcher"),
            (None, True),
        ),
    )
    def test_can_match_with_a_subset_of_headers(
        self, make_request, header_matcher, matches
    ):
        headers = {"A": "a", "B": "b"}
        request = make_request(headers=headers)

        matcher = AnyRequest.containing_headers(header_matcher)

        assert (request == matcher) is matches

    @pytest.fixture
    def make_request(self, request_class, default_params):
        def make_request(**params):
            params = dict(default_params, **params)

            return RequestBuilder.build(class_=request_class, params=params)

        return make_request

    @pytest.fixture
    def default_params(self):
        return {"url": "http://example.com/", "method": "GET", "headers": {}}

    @pytest.fixture(
        params=(
            param(Request, id="requests.Request"),
            param(PreparedRequest, id="requests.PreparedRequest"),
            param(PyramidRequest, id="pyramid.request.Request"),
            param(DummyRequest, id="pyramid.testing.DummyRequest"),
        )
    )
    def request_class(self, request):
        # Note that `request` in this context is a pytest thing
        return request.param

    @pytest.fixture(params=[True, False], ids=["fluent", "init"])
    def is_fluent(self, request):
        return request.param


class RequestBuilder:
    @classmethod
    def build(cls, class_, params):
        # Requests objects
        if issubclass(class_, Request):
            return Request(**params)

        if issubclass(class_, PreparedRequest):
            return Request(**params).prepare()

        # Pyramid objects
        environ = cls._make_environ(**params)

        if issubclass(class_, PyramidRequest):
            return PyramidRequest(environ)

        if issubclass(class_, DummyRequest):
            request = DummyRequest(
                environ, url=params["url"], headers=params["headers"]
            )
            request.method = params["method"]

            return request

        raise NotImplementedError(
            f"Don't know how to build '{class_}'"
        )  # pragma: no cover

    @classmethod
    def _make_environ(cls, method, url, headers):
        # https://www.python.org/dev/peps/pep-0333/#environ-variables

        url_parts = urlparse(url)

        environ = {
            "SERVER_PROTOCOL": "HTTP/1.0",
            "wsgi.url_scheme": url_parts.scheme,
            "REQUEST_METHOD": method,
            "HTTP_HOST": url_parts.hostname,
            "PATH_INFO": url_parts.path,
            "QUERY_STRING": url_parts.query,
        }

        for key, value in headers.items():
            environ[f"HTTP_{key.upper()}"] = value

        return environ
