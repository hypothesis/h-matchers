class UnhashableCounter:
    """Counts unhashable objects"""

    def __init__(self, items):
        self._counts = []
        self._items = []

        for item in items:
            self.add(item)

    def add(self, item):
        try:
            index = self._items.index(item)
            self._counts[index] += 1
        except ValueError:
            self._items.append(item)
            self._counts.append(1)

    def compare(self, other):
        for item, count in self:
            yield item, count, other[item]

        for item, other_count in other:
            if self[item]:
                continue

            yield item, 0, other_count

    def __getitem__(self, item):
        try:
            return self._counts[self._items.index(item)]
        except ValueError:
            return 0

    def __iter__(self):
        return zip(self._items, self._counts)

    def __eq__(self, other):
        """Are all counts equal to the counts in other"""
        for _, our_count, their_count in self.compare(other):
            if our_count != their_count:
                return False

        return True

    def __ge__(self, other):
        """Are all the counts greater or equal to the counts in other."""

        for _, our_count, their_count in self.compare(other):
            if our_count < their_count:
                return False

        return True
