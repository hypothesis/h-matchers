"""A matcher for URLs."""

from collections import Counter
from urllib.parse import parse_qsl, urlparse

from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.combination import AnyOf
from h_matchers.matcher.core import Matcher
from h_matchers.matcher.string import AnyString

# pylint: disable=too-few-public-methods,no-value-for-parameter


class AnyURL(Matcher):
    """Matches any URL."""

    STRING_OR_NONE = AnyOf([None, AnyString()])
    MAP_OR_NONE = AnyOf([None, AnyMapping()])

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
        scheme=None,
        host=None,
        path=None,
        query=None,
        fragment=None,
    ):
        """Initialize a new URL matcher.

        If a base URL is provided then the matcher will be based on that URL
        otherwise a general accepting matcher is generated.

        All other specified values will overwrite the defaults.

        Arguments (other than ``base_url``) can be literal string values, None
        or even other matchers.

        :param base_url: URL (with scheme) to base the matcher on
        :param scheme: Scheme to match (e.g. http)
        :param host: Hostname to match
        :param path: URL path to match
        :param query: Query to match (string, dict or matcher)
        :param fragment: Anchor fragment to match (e.g. "name" for "#name")
        """
        query = MultiValueQuery.normalise(query)
        if query and not isinstance(query, Matcher):
            # MultiValueQuery is guaranteed to return something we can provide
            # to AnyMapping for comparison
            query = AnyMapping.containing(query).only()

        self.parts = {
            # https://tools.ietf.org/html/rfc7230#section-2.7.3
            # scheme and host are case-insensitive
            "scheme": self._lower_if_string(scheme),
            "host": self._lower_if_string(host),
            # Others are not
            "path": path,
            "query": query,
            "fragment": fragment,
        }

        if base_url:
            # If we have a base URL, we'll take everything from there if it
            # wasn't explicitly provided in the contructor
            self._apply_defaults(
                self.parts, self.parse_url(base_url, require_scheme=True)
            )
        else:
            # Apply default matchers for everything not provided
            self._apply_defaults(self.parts, self.DEFAULTS)

        super().__init__(f"* any URL matching {self.parts} *", self._matches_url)

    @staticmethod
    def _lower_if_string(value):
        if isinstance(value, str):
            return value.lower()

        return value

    @staticmethod
    def _apply_defaults(values, defaults):
        for key, default_value in defaults.items():
            if values[key] is None:
                values[key] = default_value

    @staticmethod
    def parse_url(url_string, require_scheme=False):
        """Parse a URL into a dict for comparison.

        Parses the given URL allowing you to see how AnyURL will understand it.
        This can be useful when debugging why a particular URL does or does
        not match.

        :param url_string: URL to parse
        :param require_scheme: Make the scheme mandatory
        :raise ValueError: If scheme is mandatory and not provided
        :return: A normalised string of comparison values
        """
        url = urlparse(url_string)

        if not url.scheme and require_scheme:
            # Without a scheme `urlparse()` can't tell the difference between:
            # /example  /www.example.com and www.example.com
            # It thinks they are all paths, which might confuse a user
            raise ValueError(f"Cannot parse URL without scheme: {url_string}")

        return {
            "scheme": url.scheme.lower() if url.scheme else None,
            "host": url.netloc.lower() if url.netloc else None,
            "path": url.path or None,
            "query": MultiValueQuery.normalise(url.query),
            "fragment": url.fragment or None,
        }

    def _matches_url(self, other):
        if not isinstance(other, str):
            return False

        comparison = self.parse_url(other)

        return self.parts == comparison


class MultiValueQuery(list):
    """Normalise and represent query strings."""

    def items(self):
        """Iterate over contained items as if a dict.

        The bare minimum to appear as a mapping.
        """
        yield from self

    @classmethod
    def normalise(cls, query_comparator):
        """Get a normalised form of the representation of a query string.

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
        return f"<MultiValueQuery {super().__repr__()}>"  # pragma: no cover
