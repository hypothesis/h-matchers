from h_matchers import Any


class TestCombinationMatching:
    def test_combo(self):
        matcher = (
            Any()
            .list()
            .containing(
                [
                    Any(),
                    Any.instance_of(ValueError),
                    Any().dict().containing({"a": Any().iterable().containing([2])}),
                ]
            )
            .of_size(at_least=2)
        )

        assert matcher == [{"a": range(4), "b": None}, None, ValueError()]
