import os
import sys

from setuptools.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


class Install(install):
    """
        custom install command
        usage
            python setup.py install [-i {arg}|--index-url={arg}]
    """
    description = "install with specific pypi server"
    user_options = install.user_options + [('index-url=', 'i', "index url to download packages"),
                                           ('trusted-host=', None, "trusted host")]

    def initialize_options(self):
        install.initialize_options(self)
        # custom parameter
        self.index_url = None
        self.trusted_host = None

    def finalize_options(self):
        install.finalize_options(self)
        # custom setting
        if self.index_url is None:
            print('url not set, using default https://pypi.org/simple/')
        else:
            if self.trusted_host is None:
                print('index-url: {}, while trusted host is not set'.format(self.index_url))

    def run(self):
        # custom pip install through index_url
        for dep in self.distribution.install_requires:
            install_cmd = "pip install {} --disable-pip-version-check --no-cache-dir".format(dep)
            if self.index_url is not None:
                install_cmd += " -i {}".format(self.index_url)
            if self.trusted_host is not None:
                install_cmd += " --trusted-host={}".format(self.trusted_host)
            os.system(install_cmd)
        install.run(self)


class PyTest(TestCommand):
    """
        pytest
        usage
            python setup.py test [-a {arg}|--pytest-args={arg}]
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test"),
                    ('index-url=', 'i', "index url to download packages"),
                    ('trusted-host=', None, "trusted host")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        self.index_url = None
        self.trusted_host = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        # custom setting
        if self.index_url is None:
            print('url not set, using default https://pypi.org/simple/')
        else:
            if self.trusted_host is None:
                print('index-url: {}, while trusted host is not set'.format(self.index_url))

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        # pytest should pass list object to main, so turn it to list if there's only one option
        pytest_args = [self.pytest_args] if isinstance(self.pytest_args, basestring) else self.pytest_args
        # install requirements
        for dep in self.distribution.install_requires + self.distribution.tests_require:
            install_cmd = "pip install {} --disable-pip-version-check --no-cache-dir".format(dep)
            if self.index_url is not None:
                install_cmd += " -i {}".format(self.index_url)
            if self.trusted_host is not None:
                install_cmd += " --trusted-host={}".format(self.trusted_host)
            os.system(install_cmd)
        errno = pytest.main(pytest_args)
        sys.exit(errno)


setup(
    name="cathay-spark",
    version="1.0",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=2.7",
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=["spark"],
    entry_points={},
    tests_require=['pytest'],
    zip_safe=False,
    cmdclass={'install': Install,
              'test': PyTest}
)
