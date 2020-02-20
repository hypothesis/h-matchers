"""A fluent interface over AnyURLCore for matching URLs."""
from h_matchers.decorator import fluent_entrypoint
from h_matchers.matcher.collection import AnyMapping
from h_matchers.matcher.strings import AnyString
from h_matchers.matcher.web.url.core import AnyURLCore


class AnyURL(AnyURLCore):
    """A URL matcher with a fluent style interface."""

    # pylint: disable=function-redefined

    PRESENT_DEFAULT = {
        "scheme": AnyString(),
        "host": AnyString(),
        "path": AnyString(),
        "query": AnyMapping(),
        "fragment": AnyString(),
    }

    def _apply_field_default(self, field, value):
        if value != AnyURLCore.APPLY_DEFAULT:
            return value

        return self.PRESENT_DEFAULT[field]

    @staticmethod
    def with_scheme(scheme=AnyURLCore.APPLY_DEFAULT):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @staticmethod
    def with_host(host=AnyURLCore.APPLY_DEFAULT):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @staticmethod
    def with_path(path=AnyURLCore.APPLY_DEFAULT):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @staticmethod
    def containing_query(query=AnyURLCore.APPLY_DEFAULT):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @staticmethod
    def with_query(query=AnyURLCore.APPLY_DEFAULT):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @staticmethod
    def with_fragment(fragment=AnyURLCore.APPLY_DEFAULT):
        """Confuse pylint so it doesn't complain about fluent-endpoints."""

    @classmethod
    def matching(cls, base_url):
        """Create a URL matcher based on the given URL.

        :param base_url: URL to base the matcher on
        :return: An instance of AnyURLFluent
        """
        return AnyURL(base_url)

    @fluent_entrypoint
    def with_scheme(self, scheme=AnyURLCore.APPLY_DEFAULT):
        """Specify that this URL must have a scheme or None.

        If you pass None this will ensure the URL has no scheme.

        :param scheme: None, string or matcher for the scheme
        :return: self for fluent chaining
        """

        self.parts["scheme"] = self._apply_field_default("scheme", scheme)

        return self

    @fluent_entrypoint
    def with_host(self, host=AnyURLCore.APPLY_DEFAULT):
        """Specify that this URL must have a host or None.

        If you pass None this will ensure the URL has no host.

        :param host: None, string or matcher for the host
        :return: self for fluent chaining
        """
        self.parts["host"] = self._apply_field_default("host", host)

        return self

    @fluent_entrypoint
    def with_path(self, path=AnyURLCore.APPLY_DEFAULT):
        """Specify that this URL must have a path or None.

        If you pass None this will ensure the URL has no path.

        :param path: None, string or matcher for the path
        :return: self for fluent chaining
        """
        if path is AnyURLCore.APPLY_DEFAULT:
            self.parts["path"] = AnyString()
        else:
            self.parts["path"] = self._get_path_matcher(
                path, self.parts["scheme"], self.parts["host"]
            )

        return self

    @fluent_entrypoint
    def containing_query(self, query):
        """Specify that the query must have at least the items specified.

        :param query: A mappable to check
        :return: self for fluent chaining
        """
        self._set_query(query, exact_match=False)

        return self

    @fluent_entrypoint
    def with_query(self, query=AnyURLCore.APPLY_DEFAULT):
        """Specify that this URL must have a query or None.

        If you pass None this will ensure the URL has no query.

        :param query: None, mapping or matcher for the query
        :return: self for fluent chaining
        """
        query = self._apply_field_default("query", query)
        self._set_query(query)

        return self

    @fluent_entrypoint
    def with_fragment(self, fragment=AnyURLCore.APPLY_DEFAULT):
        """Specify that this URL must have a fragment or None.

        If you pass None this will ensure the URL has no fragment.

        :param fragment: None, string or matcher for the fragment
        :return: self for fluent chaining
        """
        self.parts["fragment"] = self._apply_field_default("fragment", fragment)

        return self
