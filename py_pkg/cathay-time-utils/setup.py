import sys

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


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
                      'pytz== 2018.5'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=["time", "date", "utils"],
    entry_points={},
    tests_require=[],
    zip_safe=False

)
