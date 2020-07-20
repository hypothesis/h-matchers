"""A matcher for URLs.

## Basic initialisation

If no arguments are given, a matcher that matches any valid URL will be
initialized:

    AnyURL()

There's a good chance you _don't_ want this however, as actual URLs are much
more flexible than you might assume. Basically any string will match.

You can limit what the URL will match by specifying the components you want to
limit:

    AnyURL(scheme='https', query={'a': 2})

## Based on a URL

If `base_url` is given it will be split into its component parts (scheme,
host, path, etc.) and a matcher based on those components being an exact match
will be initialized:

    AnyURL("http://example.com/path?a=b#anchor")

You can override any particular part in combination with a base URL:

    AnyURL("http://example.com/path", scheme=Any.of(['http', 'https']))

## Specifying a URL query

There are many ways you can specify a URL query to match:

    AnyURL(query='a=1&b=2')
    AnyURL(query={'a': '1', 'b': '2'})
    AnyURL(query=Any.mapping.containing({'a': '2'}))

Any mappable object can be used as the specification including mutli-valued
dicts like ``webob.multidict.MultiDict``. A string with multiple values for
the same key can also be used.

# Path matching

Comparing paths is tricky, particularly when comparing to bare paths without
a scheme or host. The following rules are in place to try and make this easier:

 * If you specify `host=None`, `scheme=None` the path is matched exactly as you give it
 * In all other cases the path will match with or without a leading slash

For example:

    Any.url(scheme=None, host=None, path="foo") == "/foo"  # False
    Any.url(scheme=None, host=None, path="/foo") == "foo"  # False

    Any.url(path="/foo") == "http://example.com/foo"       # True
    Any.url(path="foo") == "http://example.com/foo"        # True
    Any.url(path="/foo") == "foo"                          # True
    Any.url(path="foo") == "/foo"                          # True
"""
import re
from collections import Counter
from urllib.parse import parse_qsl, urlparse

from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.combination import AnyOf, NamedMatcher
from h_matchers.matcher.core import Matcher
from h_matchers.matcher.strings import AnyString, AnyStringMatching

# pylint: disable=too-few-public-methods,no-value-for-parameter


class AnyURLCore(Matcher):
    """Matches any URL."""

    APPLY_DEFAULT = object()
    STRING_OR_NONE = NamedMatcher("<AnyStringOrNone>", AnyOf([None, AnyString()]))
    MAP_OR_NONE = NamedMatcher("<AnyMappingOrNone>", AnyOf([None, AnyMapping()]))

    DEFAULTS = {
        "scheme": STRING_OR_NONE,
        "host": STRING_OR_NONE,
        "path": STRING_OR_NONE,
        "query": MAP_OR_NONE,
        "fragment": STRING_OR_NONE,
    }

    # pylint: disable=too-many-arguments
    # I can't see a way around it. We could use kwargs, but then auto complete
    # would be hard
    def __init__(
        self,
        base_url=None,
        scheme=APPLY_DEFAULT,
        host=APPLY_DEFAULT,
        path=APPLY_DEFAULT,
        query=APPLY_DEFAULT,
        fragment=APPLY_DEFAULT,
    ):
        """Initialize a new URL matcher.

        :param base_url: URL (with scheme) to base the matcher on
        :param scheme: Scheme to match (e.g. http)
        :param host: Hostname to match
        :param path: URL path to match
        :param query: Query to match (string, dict or matcher)
        :param fragment: Anchor fragment to match (e.g. "name" for "#name")
        """
        self.parts = {
            # https://tools.ietf.org/html/rfc7230#section-2.7.3
            # scheme and host are case-insensitive
            "scheme": self._lower_if_string(scheme),
            "host": self._lower_if_string(host),
            # `path`, `query` and `fragment` are case-sensitive
            "path": self._get_path_matcher(path, scheme, host),
            "fragment": fragment,
        }

        self._set_query(query)

        if base_url:
            self._set_base_url(base_url)
        else:
            # Apply default matchers for everything not provided
            self._apply_defaults(self.parts, self.DEFAULTS)

        super().__init__("dummy", self._matches_url)

    def __str__(self):
        contraints = {
            key: value
            for key, value in self.parts.items()
            if value is not self.DEFAULTS[key]
        }

        if not contraints:
            return "* any URL *"

        return f"* any URL matching {contraints} *"

    @classmethod
    def parse_url(cls, url_string):
        """Parse a URL into a dict for comparison.

        Parses the given URL allowing you to see how AnyURL will understand it.
        This can be useful when debugging why a particular URL does or does
        not match.

        :param url_string: URL to parse
        :raise ValueError: If scheme is mandatory and not provided
        :return: A normalised string of comparison values
        """
        url = urlparse(url_string)

        if not url.scheme and not url.netloc:
            # Without a scheme `urlparse()` assumes that the hostname is part
            # of the path, so we have to try and guess what it really was

            host, path = cls._guess_hostname_and_path(url.path)
            url = url._replace(netloc=host, path=path)

        return {
            "scheme": url.scheme.lower() if url.scheme else None,
            "host": url.netloc.lower() if url.netloc else None,
            "path": url.path or None,
            "query": MultiValueQuery.normalise(url.query),
            "fragment": url.fragment or None,
        }

    @staticmethod
    def _get_path_matcher(path, scheme, host):
        # If we are anything other than a plain string or None, use it directly
        if path is not None and not isinstance(path, str):
            return path

        # If we are matching paths alone, just return whatever we were given
        # so we match exactly. This lets the user distinguish between /path
        # and path which may be important
        if scheme is None and host is None:
            return path

        # If we got None, we need to allow ourselves to match either slash, ''
        # or None
        if path in (None, "/", ""):
            return NamedMatcher("<Path '/'>", AnyOf([None, AnyStringMatching(r"^/?$")]))

        # Otherwise construct a matcher which doesn't care about leading
        # slashes
        return NamedMatcher(
            f"'<Path '{path}'>", AnyStringMatching(f"^/?{re.escape(path)}$")
        )

    def _set_query(self, query, exact_match=True):
        if query is not self.APPLY_DEFAULT:
            query = MultiValueQuery.normalise(query)
            if query and not isinstance(query, Matcher):
                # MultiValueQuery is guaranteed to return something we can
                # provide to AnyMapping for comparison
                query = AnyMapping.containing(query)
                if exact_match:
                    query = query.only()

        self.parts["query"] = query

    def _set_base_url(self, base_url):
        # If we have a base URL, we'll take everything from there if it
        # wasn't explicitly provided in the constructor

        overlay = self.parse_url(base_url)

        path_matcher = self._get_path_matcher(
            overlay["path"], overlay["scheme"], overlay["host"]
        )
        overlay["path"] = path_matcher
        self._apply_defaults(self.parts, overlay)

    @staticmethod
    def _lower_if_string(value):
        if isinstance(value, str):
            return value.lower()

        return value

    @staticmethod
    def _apply_defaults(values, defaults, default_key=APPLY_DEFAULT):
        for key, default_value in defaults.items():
            if values[key] is default_key:
                values[key] = default_value

    @classmethod
    def _is_hostname(cls, host):
        if not host:
            return False

        if "." in host:
            return True

        return host.lower() == "localhost"

    @classmethod
    def _guess_hostname_and_path(cls, path):
        if "/" in path:
            head, tail = path.split("/", 1)
            if cls._is_hostname(head):
                return head, f"/{tail}"

        elif cls._is_hostname(path):
            return path, None

        return None, path

    def assert_equal_to(self, other):
        """Assert that the URL object is equal to another object.

        :raise AssertionError: If no match is found with details of why
        """

        if not isinstance(other, str):
            raise AssertionError("Other URL is not a string")

        comparison = self.parse_url(other)

        for key, self_value in self.parts.items():
            other_value = comparison.get(key)

            if self_value != other_value:
                raise AssertionError(f"Other '{key}' {other_value} != {self_value}")

    def _matches_url(self, other):
        try:
            self.assert_equal_to(other)
        except AssertionError:
            if self.assert_on_comparison:
                raise

            return False

        return True


class MultiValueQuery(list):
    """Normalise and represent URL queries.

    This class is for internal use only and should not be used by outside
    consumers.
    """

    def items(self):
        """Iterate over contained items as if a dict.

        The bare minimum to appear as a mapping so that we can be passed to
        `AnyMapping.contains()`.
        """
        yield from self

    @classmethod
    def normalise(cls, query_comparator):
        """Get a normalised form of the representation of a query.

        :return: None, a matcher or something suitable for AnyMapping.
        """
        if query_comparator is None:
            return None

        if isinstance(query_comparator, str):
            return cls._from_query_string(query_comparator)

        return query_comparator

    @classmethod
    def _from_query_string(cls, query_string):
        if not query_string:
            return None

        key_value = parse_qsl(query_string)

        if cls._max_key_repetitions(key_value) > 1:
            return MultiValueQuery(key_value)

        return dict(key_value)

    @classmethod
    def _max_key_repetitions(cls, key_value):
        return Counter(key for key, _ in key_value).most_common(1)[0][1]

    def __repr__(self):
        return f"<MultiValueQuery {super().__repr__()}>"
