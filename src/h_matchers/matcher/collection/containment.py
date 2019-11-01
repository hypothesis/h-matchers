"""Matchers for testing collections have specific items."""

# pylint: disable=too-few-public-methods

from h_matchers.exception import NoMatch
from h_matchers.matcher.core import Matcher


class AnyMappableWithItems(Matcher):
    """Matches any container which contains all specified key value pairs."""

    def __init__(self, key_values):
        super().__init__(
            f"* contains {key_values} *",
            lambda other: self._contains_values(other, key_values),
        )

    @classmethod
    def _contains_values(cls, container, key_values):
        if not hasattr(container, "items"):
            return False

        for key, value in key_values.items():
            if key not in container:
                return False

            if container[key] != value:
                return False

        return True


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
        """Can every item can be uniquely matched to something in container?.

        :param container: An iterable of items to check over
        :param items_to_match: An iterable of items to try and match
        :return: A boolean indicating whether each item can be matched
        """

        try:
            container = list(container)
        except TypeError:
            # Not even an iterable
            return False

        try:
            cls._is_solvable(cls._cross_match(container, items_to_match))
        except NoMatch:
            return False

        return True

    @classmethod
    def _cross_match(cls, container, items_to_match):
        """Find all possible matches as sets of positions.

        Look through each item and list every position in the `container` that
        they match.
        :yields: Sets of positions which match a particular item
        """
        for item in items_to_match:
            constraint_set = set()
            for other_pos, other_item in enumerate(container):
                if item == other_item:
                    constraint_set.add(other_pos)

            yield constraint_set

    @classmethod
    def _is_solvable(cls, constraints):
        """Works out if a set of constraints are mutually incompatible.

        Takes a list of sets of positions and works out if each set can be
        reduced to a single value which doesn't appear in any other set.

        This indicates that we can match each item to a unique item in the
        parent object, rather than having multiple objects matching the same
        thing.

        :param constraints: An iterable of sets of positions
        :raises NoMatch: If the sets are not resolvable
        :return: True if the sets are resolvable
        """
        # Order items by how many matches they have (ascending)
        sorted_constraints = sorted(constraints, key=len)

        if not sorted_constraints:
            # If there are no items to resolve, we have a match!
            return True

        head, tail = sorted_constraints[0], sorted_constraints[1:]

        # Otherwise we look at each possible match for the first item in turn
        for this_match in head:
            # Pick a match for this item, and then ban every other item from
            # matching this one
            try:
                return cls._is_solvable((set(item) - {this_match} for item in tail))
            except NoMatch:
                # Well this branch didn't work out for some reason...
                continue

        # Oh... no branches worked out
        raise NoMatch()
