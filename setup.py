#!/usr/bin/env python
# coding: utf-8

import drip

# Require setuptools. See http://pypi.python.org/pypi/setuptools for
# installation instructions, or run the ez_setup script found at
# http://peak.telecommunity.com/dist/ez_setup.py
from setuptools import setup

# Load the test requirements. These are in a separate file so they can
# be accessed from Travis CI and tox.
with open("test-requirements.txt") as fd:
    tests_require = list(fd)


setup(
    name="drip",
    version=drip.__version__,
    author="Bob Green",
    author_email="bgreen@litl.com",
    license="MIT",
    url="https://github.com/litl/drip",
    description="A library for exploring multivariate datasets",
    py_modules=["drip"],

    setup_requires=[
        "pytest==2.7.2"
    ],

    tests_require=['pytest'],
    cmdclass = {'test': pytest},

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ]
)
