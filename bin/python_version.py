#!/usr/bin/env python

"""A script for printing supported python versions in various formats."""

import json
import os
import re
from argparse import ArgumentParser
from collections import OrderedDict

parser = ArgumentParser("Dump the versions of Python in various formats")
parser.add_argument(
    "--style",
    required=True,
    help="The style to output the codes (`tox`, `gha`, `headline`)",
)

parser.add_argument(
    "--first",
    default=False,
    action="store_const",
    const=True,
    help="Only return the first item found",
)

parser.add_argument(
    "--floating",
    default=False,
    action="store_const",
    const=True,
    help="Mark the last digit of marked versions with 'x'",
)

parser.add_argument(
    "--include-future",
    default=False,
    action="store_const",
    const=True,
    help="Include aspirational versions of Python",
)


class PyenvVersionFile:
    """A pyenv version file.

    This pyenv version file can accept tags in the form of comments like this:

        3.8.8 # future floating

    Currently accepted tags (format dependent) are:

     * future - Included in local testing but not required to pass CI
     * floating - Use a wild build version where supported
    """

    def __init__(self, file_name):
        if not os.path.isfile(file_name):
            raise FileNotFoundError("Expected to find version file '%s'." % file_name)

        self.file_name = file_name
        self.versions = self._parse_version_file(self.file_name)

    def filter_versions(self, exclude=None, floating=False):
        """Return a dict of digits and tags which don't match the tags."""

        exclude = set(exclude or [])

        for digits, tags in self.versions.items():
            if tags & exclude:
                continue

            if floating and "floating" in tags:
                digits = list(digits)
                digits[-1] = "x"

            yield digits

    @classmethod
    def format(cls, raw_digits, style):
        """Get the python versions in a variety of styles.

        `plain`: e.g. 3.8.8 3.9.2

        `tox`: e.g. py27,py36,py37

        Which can be used in comprehensions like this:

            tox -e {py27,py36}-tests

        `gha`: e.g. ["3.6.12", "3.8.8", "3.9.2"]

        This is valid JSON and can be included in scripts.
        """

        if style == "plain":
            return " ".join(".".join(digits) for digits in raw_digits)

        if style == "tox":
            return ",".join("py" + "".join(digits[:2]) for digits in raw_digits)

        if style == "gha":
            codes = []
            for digits in raw_digits:
                codes.append(".".join(digits))

            return json.dumps(codes)

        if style == "classifier":
            rows = []
            for digits in reversed(raw_digits):
                rows.append(
                    "    Programming Language :: Python :: "
                    + ".".join(digits[:2])
                    + "\n"
                )

            return "".join(rows)

        raise ValueError("Unsupported style '%s'" % style)

    _PYTHON_VERSION = re.compile(r"^(\d+).(\d+).(\d+)$")

    @classmethod
    def _parse_version_file(cls, file_name):
        # Add support for older versions of Python to guarantee ordering
        versions = OrderedDict()

        with open(file_name) as handle:
            for line in handle:
                comment = ""

                if "#" in line:
                    comment = line[line.index("#") + 1 :]
                    line = line[: line.index("#")]

                line = line.strip()
                if not line:
                    continue

                match = cls._PYTHON_VERSION.match(line)
                if not match:
                    raise ValueError(f"Could not parse python version: '{line}'")

                tags = set(part.strip() for part in comment.strip().split("#"))
                tags.discard("")  # Drop anything caused by repeated spaces

                versions[match.groups()] = tags

        return versions


if __name__ == "__main__":
    args = parser.parse_args()

    version_file = PyenvVersionFile(os.path.abspath(".python-version"))

    version_digits = list(
        version_file.filter_versions(
            exclude=None if args.include_future else {"future"}, floating=args.floating
        )
    )

    if args.first:
        version_digits = [version_digits[0]]

    # Don't emit a new line to make this easy to splat into the middle of
    # other scripts
    print(version_file.format(version_digits, args.style), end="")
