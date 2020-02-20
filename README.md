# h-matchers

Test objects which pass equality checks with other objects

Usage
-----

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
    AnyString.containing('foo'), 
    AnyString.containing('bar')
])
```

### Comparing to collections
You can make basic comparisons to collections as follows:

```python
Any.iterable()
Any.list()
Any.set()
```

You can specify a custom class with:

```python
Any.iterable.of_type(MyCustomList)
```

#### Specifying size

You can also chain on to add requirements for the size.

```python
Any.iterable.of_size(4)
Any.list.of_size(at_least=3)
Any.set.of_size(at_most=5)
Any.set.of_size(at_least=3, at_most=5)
```

#### Specifying specific content

You can require an iterable to have a minimum number of items, with repetitions
, optionally in order:

```python
Any.iterable.containing([1])
Any.list.containing([1, 2, 2])
Any.list.containing([1, 2, 2]).in_order()
```

This will match if the sequence is found any where in the iterable.

You can also say that there cannot be any extra items in the iterable:

```python
Any.set.containing({2, 3, 4}).only()
Any.list.containing([1, 2, 2, 3]).only().in_order()
```

All of this should work with non-hashable items too as long as the items test
as equal:

```python
Any.set.containing([{'a': 1}, {'b': 2}])
```

#### Specifying every item must match something

You can specify that every item in the collection must match a certain item.
You can also pass matchers to this:

```python
Any.list.comprised_of(Any.string).of_size(6)
Any.iterable.comprised_of(True)
```

### Comparing to dicts

Basic comparisons are available:

```python
Any.iterable()
Any.mapping()
Any.dict()
```

### Most things for collections go for dicts too

```python
Any.dict.of_size(at_most=4)
Any.dict.containing(['key_1', 'key_2']).only()
```

### You can test for key value pairs

```python
Any.dict.containing({'a': 5, 'b': 6})
Any.dict.containing({'a': 5, 'b': 6}).only()
```

### You can compare against any mappable including multi-value dicts

This is useful for dict-like objects which may have different behavior and
semantics to regular dicts. For example: objects which support multiple values
for the same key.

```python
Any.mapping.containing(MultiDict(['a', 1], ['a', 2]))
```

### Comparing to URLs

The URL matcher provides a both a kwargs interface and a fluent style interface which is a little
more verbose but provides more readable results.

You can construct matchers directly from URLs:

```python
Any.url("http://example.com/path?a=b#anchor")
Any.url.matching("http://example.com/path?a=b#anchor")
```

You can also construct URL matchers manually:

```python
Any.url(host='www.example.com', path='/path')
Any.url.matching('www.example.com').with_path('/path')

Any.url(scheme=Any.string.containing('http'), query={'a': 'b'}, fragment='anchor')
Any.url.with_scheme(Any.string.containing('http')).with_query({'a': 'b'}).with_fragment('anchor')
```

Or mix and match, here the separate `host=Any()` argument overrides the `example.com` in the URL and allows URLs with any host to match:
```python
Any.url("http://example.com/path?a=b#anchor", host=Any())  
Any.url.matching("http://example.com/path?a=b#anchor").with_host(Any()) 
```

#### Matching URL queries

You can specify the query in a number of different ways:

```python
Any.url(query='a=1&a=2&b=2')
Any.url.with_query('a=1&a=2&b=2')

Any.url(query={'a': '1', 'b': '2'})
Any.url.with_query({'a': '1', 'b': '2'})

Any.url(query=[('a', '1'), ('a', '2'), ('b', '2')])
Any.url.with_query([('a', '1'), ('a', '2'), ('b', '2')])

Any.url(query=Any.mapping.containing({'a': '1'}))
Any.url.containing_query({'a': '1'})
```

#### Specify that a component must be present

With the fluent interface you can specify that a URL must contain a certain 
part without specifying what that part has to be:

```python
AnyURL.with_scheme()
AnyURL.with_host()
AnyURL.with_path()
AnyURL.with_query()
AnyURL.with_fragment()
```

Hacking
-------

### Installing h-matchers in a development environment

#### You will need

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.
  On Ubuntu follow the Basic GitHub Checkout method.

#### Clone the git repo

```terminal
git clone https://github.com/hypothesis/h-matchers.git
```

This will download the code into a `h-matchers` directory
in your current working directory. You need to be in the
`h-matchers` directory for the rest of the installation
process:

```terminal
cd h-matchers
```

#### Run the tests

```terminal
make test
```

**That's it!** You’ve finished setting up your h-matchers
development environment. Run `make help` to see all the commands that're
available for linting, code formatting, packaging, etc.

### Updating the Cookiecutter scaffolding

This project was created from the
https://github.com/hypothesis/h-cookiecutter-pypackage/ template.
If h-cookiecutter-pypackage itself has changed since this project was created, and
you want to update this project with the latest changes, you can "replay" the
cookiecutter over this project. Run:

```terminal
make template
```

**This will change the files in your working tree**, applying the latest
updates from the h-cookiecutter-pypackage template. Inspect and test the
changes, do any fixups that are needed, and then commit them to git and send a
pull request.

If you want `make template` to skip certain files, never changing them, add
these files to `"options.disable_replay"` in
[`.cookiecutter.json`](.cookiecutter.json) and commit that to git.

If you want `make template` to update a file that's listed in `disable_replay`
simply delete that file and then run `make template`, it'll recreate the file
for you.
