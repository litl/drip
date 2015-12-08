#!/usr/bin/env python
# coding: utf-8

import drip

# Require setuptools. See http://pypi.python.org/pypi/setuptools for
# installation instructions, or run the ez_setup script found at
# http://peak.telecommunity.com/dist/ez_setup.py
from setuptools import setup

version = drip.__version__
download_url = "https://github.com/litl/drip/tarball/v{0}".format(version)

setup(
    name="drip",
    version=version,
    author="Bob Green",
    author_email="bgreen@litl.com",
    license="MIT",
    url="https://github.com/litl/drip",
    download_url=download_url,
    description="A library for exploring multivariate datasets",
    py_modules=["drip"],

    setup_requires=[
        "pytest==2.8.4",
        "bitarray==0.8.1",
    ],
    install_requires=[
        "bitarray==0.8.1"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ]
)
