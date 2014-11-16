#!/usr/bin/env python

import os
try:
    from setuptools import setup, find_packages

except ImportError:
    from distutils.core import setup, find_packages


# _PACKAGES = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

version = '0.0.1'

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

# DO NOT put non-ASCII character in setup, installation with pip may fail if LC_ALL="C"
setup(
    name='RedSparrow',
    version=version,
    packages=['redsparrow'],
    description='Plagiarism checker',
    author='Teleinformatyka',
    maintainer='Teleinformatyka',
    maintainer_email='Teleinformatyka@gmail.com',
    classifiers=['Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    long_description=open('README.rst').read(),
    install_requires=required,
)
