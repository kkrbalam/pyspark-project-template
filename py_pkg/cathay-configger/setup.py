import sys

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

print find_packages
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
    tests_require=[]
)
