from __future__ import print_function
import os
import sys
from setuptools import setup, Command
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


class Install(install):
    """
        pytest
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


class Clean(Command):
    """
        custom clean command
        usage:
            python setup.py clean [-e|--egg]
    """
    description = "Cleans build files"
    user_options = [('egg', 'e', "Arguments to clean with .eggs folder")]

    def initialize_options(self):
        self.egg = None

    def finalize_options(self):
        if self.egg is None:
            print('not deleting .eggs folder')

    def run(self):
        cmd = dict(
            build="find ./ -name 'build' -exec rm -rf {} +",
            egg_info="find ./ -name '*.egg-info' -exec rm -rf {} +",
            dist="find ./ -name 'dist' -exec rm -rf {} +"
        )
        if self.egg is not None:
            cmd['eggs'] = "find ./ -name '.eggs' -exec rm -rf {} +"

        for key in cmd:
            print('remove {} folder ...'.format(key))
            os.system(cmd[key])


class InstallLibs(Command):
    """
        install packages in py_pkg
        usage:
            python setup.py lib [-p py_pkg | --lib-path=py_pkg
    """
    description = "Install py_pkg libs"
    user_options = [('lib-path=', 'p', "Arguments to install libs in py_pkg"),
                    ('index-url=', 'i', "index url to download packages")]

    def initialize_options(self):
        self.lib_path = None
        self.index_url = None

    def finalize_options(self):
        # custom setting
        default_url = 'https://pypi.org/simple/'
        if self.index_url is None:
            print('url not set, using: {}'.format(default_url))
            self.index_url = default_url

    def run(self):
        install_cmd = "python setup.py install -i {}".format(self.index_url)
        project_dir = os.getcwd()
        if self.lib_path is not None:
            for pkg in os.listdir(self.lib_path):
                os.chdir(os.path.join(project_dir, self.lib_path, pkg))
                os.system(install_cmd)
        else:
            print('set py_pkg path')


setup(
    # index_url= 'http://pypi.python.org/simple/',
    entry_points={
        'console_scripts': [
            'second-entry=project_template.job.second_entry:main'
        ]
    },
    cmdclass={'install': Install,
              'test': PyTest,
              'clean': Clean,
              'lib': InstallLibs}
)
