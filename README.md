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

* [Matching data structures](docs/matching-data-structures.md) - For details
  of matching collections and objects
* [Matching web objects](docs/matching-web.md) - For details about matching
  URLs, and web requests

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
