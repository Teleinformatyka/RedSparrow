#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.0.1'

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

# DO NOT put non-ASCII character in setup, installation with pip may fail if LC_ALL="C"
setup(
    name='RedSparrow',
    version=version,
    packages=['RedSparrow'],
    description='',
    author='',
    maintainer='',
    maintainer_email='',
    classifiers=['Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    install_requires=required,
)
