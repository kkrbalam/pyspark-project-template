from __future__ import print_function
import os
import sys
from setuptools import setup, Command
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """
        pytest
        usage
            python setup.py test [-a {arg}|--pytest-args={arg}]
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        # pytest should pass list object to main, so turn it to list if there's only one option
        pytest_args = [self.pytest_args] if isinstance(self.pytest_args, basestring) else self.pytest_args
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
    user_options = [('lib-path=', 'p', "Arguments to install libs in py_pkg")]

    def initialize_options(self):
        self.lib_path = None

    def finalize_options(self):
        pass

    def run(self):
        install_cmd = "python setup.py install"
        project_dir = os.getcwd()
        if self.lib_path is not None:
            for pkg in os.listdir(self.lib_path):
                os.chdir(os.path.join(project_dir, self.lib_path, pkg))
                os.system(install_cmd)
        else:
            print('set py_pkg path')


setup(
    entry_points={
        'console_scripts': [
            'second-entry=project_template.job.second_entry:main'
        ]
    },
    cmdclass={'test': PyTest,
              'clean': Clean,
              'lib': InstallLibs}
)
