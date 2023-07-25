"""Matchers for testing collections have specific items."""

from h_matchers.matcher.core import Matcher


class AnyIterableWithItemsInOrder(Matcher):
    """Matches any item which contains certain elements in order."""

    def __init__(self, items_to_match):
        super().__init__(
            f"* contains {items_to_match} in any order *",
            lambda other: self._contains_in_order(other, items_to_match),
        )

    @classmethod
    def _contains_in_order(cls, container, items_to_match):
        """Check if each item can be found in order in the container.

        :param container: An iterable of items to check over
        :param items_to_match: An iterable of items to try and match
        :return: A boolean indicating whether each item can be matched
        """
        # Ensure we can work with generators
        try:
            container = list(container)
        except TypeError:
            # It's not even iterable
            return False

        last_index = None

        for item in items_to_match:
            try:
                last_index = (
                    container.index(item)
                    if last_index is None
                    else container.index(item, last_index)
                ) + 1
            except ValueError:
                return False

        return True


class AnyIterableWithItems(Matcher):
    """Matches any item which contains certain elements."""

    def __init__(self, items_to_match):
        super().__init__(
            f"* contains {items_to_match} in any order *",
            lambda other: self._contains_in_any_order(other, items_to_match),
        )

    @classmethod
    def _contains_in_any_order(cls, container, items_to_match):
        # See `containment.md` for a description of this algorithm
        try:
            container = list(container)
        except TypeError:
            # Not even an iterable
            return False

        # Create a tuple of tuples containing the matcher index, and the set of all
        # possible indices of items from the container which could be a match. From
        # here on in, we deal entirely with indices, no matcher matching will happen
        # again.
        unsolved = tuple(
            (
                match_index,
                {
                    item_index
                    for item_index, item in enumerate(container)
                    if item == matcher
                },
            )
            for match_index, matcher in enumerate(items_to_match)
        )

        if matched_item_indices := cls._solve(unsolved=unsolved, solved=[]):
            # Update any matchers to have the correct last history entry.

            # For each item in items to match which is matcher, set its history
            # as if it had just matched against the corresponding item in
            # container. This will fix the history we mess up during with
            # matching operations creating unsolved above.
            for item_to_match, matched_item_index in zip(
                items_to_match, matched_item_indices
            ):
                if isinstance(item_to_match, Matcher):
                    item_to_match.matched_to = [container[matched_item_index]]

            return True

        return False

    @classmethod
    def _solve(cls, unsolved: tuple, solved: list):
        """Get the first solution as a mapping from match to item index.

        :param unsolved: Tuple of match indicies to set of target indicies
        :param solved: Tuple of match indicies to target indicies
        :return: Tuple of matching target indices
        """

        # If there are no more unsolved parts, we are done! This is the recusion
        # base case.
        if not unsolved:
            return tuple(item_index for _match_index, item_index in sorted(solved))

        # Sort our unsolved parts by the number of possibilities they have.
        # Solve those with fewer possibilities first as they are less free.
        # Separate out the head as the most constrained.
        head, *tail = sorted(unsolved, key=lambda item: len(item[1]))
        head_pos, head_possibilities = head

        for chosen_match in head_possibilities:
            # For every possible match from the head we recurse in...

            if result := cls._solve(
                # Create a new unsolved tuple by removing the match from all the
                # other unsolved parts. It's no longer a possibility for them
                # another part has matched it against the head.
                unsolved=tuple(
                    (pos, possibility - {chosen_match}) for pos, possibility in tail
                ),
                # Extend the solved parts with the new solution
                solved=solved + [(head_pos, chosen_match)],
            ):
                return result

        return None


class AnyMappingWithItems(Matcher):
    """Matches any mapping contains specified key value pairs."""

    def __init__(self, key_values):
        super().__init__(
            f"* contains {key_values} *",
            lambda other: self._contains_values(other, key_values),
        )

    @classmethod
    def _contains_values(cls, container, key_values):
        # Direct dict comparison is 200-300x faster than the more generic
        # fallback, which runs a search algorithm. So if we are comparing
        # to a plain dict, it's much better
        if isinstance(container, dict):
            return cls._dict_comparison(container, key_values)

        if hasattr(container, "items"):
            return cls._mapping_comparison(container, key_values)

        return False

    @classmethod
    def _dict_comparison(cls, container, key_values):
        for key, value in key_values.items():
            if key not in container:
                return False

            # Do the comparison backwards to give matchers a chance to kick in
            if value != container[key]:
                return False

        return True

    @classmethod
    def _mapping_comparison(cls, container, key_values):
        flat_key_values = cls._normalise_items(key_values)
        items_to_compare = cls._normalise_items(container)

        return items_to_compare == AnyIterableWithItems(flat_key_values)

    @classmethod
    def _normalise_items(cls, mapping):
        """Handle badly behaved items() implementations returning lists."""
        return tuple((k, v) for k, v in mapping.items())
