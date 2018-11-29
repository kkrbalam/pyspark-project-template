from __future__ import print_function
import os
import sys
from setuptools import setup, Command
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


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


class InstallLibs(Command):
    """
        install packages in py_pkg
        usage:
            python setup.py lib [-p py_pkg | --lib-path=py_pkg
    """
    description = "Install py_pkg libs"
    user_options = [('lib-path=', 'p', "Arguments to install libs in py_pkg"),
                    ('index-url=', 'i', "index url to download packages"),
                    ('trusted-host=', None, "trusted host")]

    def initialize_options(self):
        self.lib_path = None
        self.index_url = None
        self.trusted_host = None

    def finalize_options(self):
        # custom setting
        default_url = 'https://pypi.org/simple/'
        if self.index_url is None:
            print('url not set, using: {}'.format(default_url))
            self.index_url = default_url
        if self.trusted_host is None:
            print('trusted host not set, might lead to unexpected result')

    def run(self):
        install_cmd = "python setup.py install"
        if self.index_url is not None:
            install_cmd += " -i {}".format(self.index_url)
        if self.trusted_host is not None:
            install_cmd += " --trusted-host={}".format(self.trusted_host)

        project_dir = os.getcwd()
        if self.lib_path is not None:
            for pkg in os.listdir(self.lib_path):
                print(os.path.join(project_dir, self.lib_path, pkg))
                os.chdir(os.path.join(project_dir, self.lib_path, pkg))
                os.system(install_cmd)
        else:
            print('set py_pkg path')


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


setup(
    entry_points={
        'console_scripts': [
            'second-entry=project_template.job.second_entry:main'
        ]
    },
    cmdclass={'install': Install,
              'test': PyTest,
              'lib': InstallLibs,
              'clean': Clean}
)
