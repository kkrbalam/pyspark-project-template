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
    user_options = install.user_options + [('index-url=', 'i', "index url to download packages")]

    def initialize_options(self):
        install.initialize_options(self)
        # custom parameter
        self.index_url = None

    def finalize_options(self):
        install.finalize_options(self)
        # custom setting
        default_url = 'https://pypi.org/simple/'
        if self.index_url is None:
            print('url not set, using: {}'.format(default_url))
            self.index_url = default_url

    def run(self):
        # custom pip install through index_url
        for dep in self.distribution.install_requires:
            os.system(("pip install {dep} -i {url} --disable-pip-version-check "
                       "--no-cache-dir").format(dep=dep, url=self.index_url))
        install.run(self)


class PyTest(TestCommand):
    """
        pytest
        usage
            python setup.py test [-a {arg}|--pytest-args={arg}]
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test"),
                    ('index-url=', 'i', "index url to download packages")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        self.index_url = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        # custom setting
        default_url = 'https://pypi.org/simple/'
        if self.index_url is None:
            print('url not set, using: {}'.format(default_url))
            self.index_url = default_url

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        # pytest should pass list object to main, so turn it to list if there's only one option
        pytest_args = [self.pytest_args] if isinstance(self.pytest_args, basestring) else self.pytest_args
        # install requirements
        for dep in self.distribution.install_requires + self.distribution.tests_require:
            os.system(("pip install {dep} -i {url} --disable-pip-version-check "
                       "--no-cache-dir").format(dep=dep, url=self.index_url))
        errno = pytest.main(pytest_args)
        sys.exit(errno)


setup(
    name="cathay-configger",
    version="1.0",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=2.7",
    install_requires=['pyhocon>=0.3.38'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=["configger"],
    entry_points={},
    tests_require=['pytest'],
    zip_safe=False,
    cmdclass={'install': Install,
              'test': PyTest}
)
