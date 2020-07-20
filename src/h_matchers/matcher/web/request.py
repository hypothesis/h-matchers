"""A matcher that matches various request objects in HTTP type libraries."""
from copy import deepcopy

from h_matchers.decorator import fluent_entrypoint
from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.core import Matcher
from h_matchers.matcher.strings import AnyString
from h_matchers.matcher.web.url import AnyURL

# pylint: disable=too-few-public-methods


class _LibraryNotAvailable:
    """Substitute for missing libraries."""


try:  # pylint: disable=too-many-try-statements
    # We don't require our clients to install every request library we support
    # so we will enable it if it's around, and carry on without if it's not
    from requests import PreparedRequest as RequestsPreparedRequest
    from requests import Request as RequestsRequest

except ImportError:  # pragma: no cover
    RequestsRequest, RequestsPreparedRequest = (
        _LibraryNotAvailable,
        _LibraryNotAvailable,
    )

try:  # pylint: disable=too-many-try-statements
    from pyramid.request import Request as PyramidRequest
    from pyramid.testing import DummyRequest as PyramidDummyRequest

except ImportError:  # pragma: no cover
    PyramidDummyRequest, PyramidRequest = _LibraryNotAvailable, _LibraryNotAvailable


# pylint: disable=function-redefined


class AnyRequest(Matcher):  # pragma: no cover
    """Matching object for request type objects.

    Currently supported request objects:

     * `requests.Request`
     * `requests.PreparedRequest`
     * `pyramid.request.Request`
     * `pyramid.testing.Request`
    """

    # Use a set here as an optimisation for when many of these items are
    # instances of `_LibraryNotAvailable`
    SUPPORTED_TYPES = tuple(
        {RequestsRequest, RequestsPreparedRequest, PyramidRequest, PyramidDummyRequest}
    )

    method = None
    url = None
    headers = None

    def __init__(self, method=..., url=..., headers=None):
        self.with_method(method)
        self.with_url(url)
        self.with_headers(headers)

        super().__init__("*dummy*", self._matches_request)

    @classmethod
    def containing_headers(cls, headers):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @classmethod
    def with_headers(cls, header=...):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @classmethod
    def with_method(cls, method=...):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @classmethod
    def with_url(cls, url=...):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @fluent_entrypoint
    def containing_headers(self, headers):
        """Specify the request must have at least the headers specified.

        :param headers: A mappable of headers to match
        """
        self.headers = AnyMapping.containing(headers)

    @fluent_entrypoint
    def with_headers(self, headers=...):
        """Specify the request must have headers.

        This method will remove 'Host' from the set of headers as some
        libraries add it before sending, and it's mostly noise.

        :param headers: A mappable of headers or matcher to match exactly
        """
        if headers is ...:
            self.headers = AnyMapping.of_size(at_least=1)

        elif isinstance(headers, Matcher):
            self.headers = headers

        elif headers is not None:
            self.headers = AnyMapping.containing(headers).only()

    @fluent_entrypoint
    def with_method(self, method=...):
        """Specify the request must have a method.

        :param method: A string or matcher for the method
        """
        if method is ...:
            self.method = AnyString()

        elif isinstance(method, str):
            self.method = method.upper()

        elif method is not None:
            self.method = method

    @fluent_entrypoint
    def with_url(self, url=...):
        """Specify the request must have a URL.

        :param url: A string or matcher for the URL
        """
        if url is ...:
            self.url = AnyURL()

        elif isinstance(url, str):
            self.url = AnyURL.matching(url)

        elif url is not None:
            self.url = url

    def assert_equal_to(self, other):
        """Assert that the request object is equal to another object.

        :raise AssertionError: If no match is found with details of why
        """
        if not isinstance(other, self.SUPPORTED_TYPES):
            raise AssertionError(
                f"Unknown request type '{type(other)}'. For a request type to be "
                "compared it must be supported and loaded."
            )

        if self.method is not None and self.method != other.method.upper():
            raise AssertionError(f"Method '{other.method}' != '{self.method}'")

        if self.url is not None:
            self.url.assert_equal_to(other.url)

        if self.headers is not None:
            other_headers = self._comparison_headers(other)
            if self.headers != other_headers:
                raise AssertionError(f"Headers {other_headers} != {self.headers}")

    @classmethod
    def _comparison_headers(cls, other):
        if isinstance(other, PyramidRequest):
            headers = deepcopy(other.headers)
            headers.pop("Host")

            return headers

        return other.headers

    def _matches_request(self, other):
        try:
            self.assert_equal_to(other)
        except AssertionError:
            if self.assert_on_comparison:
                raise
            return False

        return True

    def __str__(self):
        details = ""
        if self.method:
            details += f" method:{self.method}"

        if self.url:
            details += f" url:{self.url}"

        if self.headers is not None:
            details += f" headers={self.headers}"

        return f"<{self.__class__.__name__}{details}>"
