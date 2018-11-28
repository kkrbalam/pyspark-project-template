import os
import sys

from setuptools.command.install import install
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


setup(
    name="cathay-time-utils",
    version="1.0",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=2.7",
    install_requires=['python-dateutil==2.7.3',
                      'pytz==2018.5'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=["time", "date", "utils"],
    entry_points={},
    tests_require=['pytest'],
    zip_safe=False,
    cmdclass={'install': Install}
)
