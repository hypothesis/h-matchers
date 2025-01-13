<a href="https://github.com/hypothesis/h-matchers/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/h-matchers/ci.yml?branch=main"></a>
<a href="https://pypi.org/project/h-matchers"><img src="https://img.shields.io/pypi/v/h-matchers"></a>
<a><img src="https://img.shields.io/badge/python-3.12 | 3.11 | 3.10 | 3.9-success"></a>
<a href="https://github.com/hypothesis/h-matchers/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# h-matchers

Test objects which pass equality checks with other objects.

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

## Setting up Your h-matchers Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/h-matchers.git
cd h-matchers
make help
```

## Releasing a New Version of the Project

1. First, to get PyPI publishing working you need to go to:
   <https://github.com/organizations/hypothesis/settings/secrets/actions/PYPI_TOKEN>
   and add h-matchers to the `PYPI_TOKEN` secret's selected
   repositories.

2. Now that the h-matchers project has access to the `PYPI_TOKEN` secret
   you can release a new version by just [creating a new GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
   Publishing a new GitHub release will automatically trigger
   [a GitHub Actions workflow](.github/workflows/pypi.yml)
   that will build the new version of your Python package and upload it to
   <https://pypi.org/project/h-matchers>.

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request
