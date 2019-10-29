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

assert [1, 2, 3] == Any.iterable()
assert [1, 2, 3] == Any.list()
assert List(1, 2) == Any.iterable.of_type(List)

assert [1, 2, 3] == Any.list.of_size(3)
assert [1, 2] == Any.iterable.of_size(at_least=1, at_most=3)

# For order independent checks 
assert [1, 2, 3, 1] == Any.set.containing([1, 1, 2, 3])  # Respecting count!
assert [3, 2, 1] == Any.list.containing[[1, 2, 3])
assert {'a': 1} == Any.dict.containing(['a'])

# All in one to say only these items
assert [2, 1, 3] == Any.list.containing({1, 2, 3}).only()

# For order dependent checks add `in_order()`
assert [3, 2, 1] != Any.list.containing([1, 2, 3]).in_order()

# Assert each item must match something (can be another matcher)
assert ["a duck", "a horse"] == Any.list.comprised_of(Any.string.containing("a"))
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
