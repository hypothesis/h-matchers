## Usage

```python
from h_matchers import Any
import re

assert [1, 2, ValueError(), print, print] == [
        Any(),
        Any.int(),
        Any.instance_of(ValueError),
        Any.function(),
        Any.callable()
    ]

assert ["easy", "string", "matching"] == [
        Any.string(),
        Any.string.containing("in"),
        Any.string.matching('^.*CHING!', re.IGNORECASE)
    ]

assert "http://www.example.com?a=3&b=2" == Any.url(
    host='www.example.com', query=Any.mapping.containing({'a': 3}))

assert 5 == Any.of([5, None])

assert "foo bar" == All.of([
    Any.string.containing('foo'),
    Any.string.containing('bar')
])

assert user == Any.object.of_type(MyUser).with_attrs({"name": "Username"})

assert "http://example.com/path" == Any.url.with_host("example.com")

assert prepared_request == (
    Any.request
    .with_url(Any.url.with_host("example.com"))
    .containing_headers({'Content-Type': 'application/json'})
)

# ... and lots more
```

For more details see:

* [Matching data structures](https://github.com/hypothesis/h-matchers/blob/main/docs/matching-data-structures.md) - For details
  of matching collections and objects
* [Matching web objects](https://github.com/hypothesis/h-matchers/blob/main/docs/matching-web.md) - For details about matching
  URLs, and web requests
* [Matching numbers](https://github.com/hypothesis/h-matchers/blob/main/docs/matching-numbers.md) - For details about matching
  ints, floats etc. with conditions
