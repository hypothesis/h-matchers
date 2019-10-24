import os

from setuptools import find_packages, setup
from setuptools.config import read_configuration


class Package:
    def __init__(self, config):
        metadata = config['metadata']
        options = config['options']

        self.options = options
        self.name = metadata['name']
        self.version = metadata['version']

    def tests_require(self):
        return self.options['tests_require'] + self.options['install_requires']

    def read_egg_version(self):
        pkg_info_file = None
        # PKG-INFO can be in different places depending on whether we are a
        # source distribution or a checked out copy etc.
        for location in [
                'PKG-INFO',
                'src/' + self.name + ".egg-info/PKG-INFO",
                self.name + ".egg-info/PKG-INFO",
            ]:
            if os.path.isfile(location):
                pkg_info_file = location

        if not pkg_info_file:
            return None

        with open(pkg_info_file) as fh:
            for line in fh:
                if line.startswith("Version"):
                    return line.strip().split("Version: ")[-1]

    def get_version(self, build_var="BUILD"):
        # If we have a build argument we should honour it no matter what
        build = os.environ.get(build_var)
        if build:
            return self.version + "." + build

        # If not, we should try and read it from the .egg-info/ data

        # We need to do this for source distributions, as setup.py is re-run when
        # installed this way, and we would always get 'dev0' as the version
        # Wheels and binary installs don't work this way and read from PKG-INFO
        # for them selves
        egg_version = self.read_egg_version()
        if egg_version:
            return egg_version

        # Otherwise create a 'dev' build which will be counted by pip as 'later'
        # than the major version no matter what
        return self.version + ".dev0"


package = Package(read_configuration('setup.cfg'))

setup(
    # Metadata
    # https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
    version=package.get_version(),

    # Contents and dependencies
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    # Read the MANIFEST.in
    include_package_data=True,

    # Add support for pip install .[tests]
    extras_require={"tests": package.tests_require()},

    tests_require=package.tests_require(),
)
