#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# What packages are required for this module to be executed?
with open('requirements.in') as requirements:
    REQUIRED = []
    for raw_line in requirements:
        line = raw_line.strip()
        if line:
            REQUIRED.append(line)

# Where the magic happens:
setup(
    name='kizuna',
    python_requires='>=3.6.0',
    package_dir={'': 'src'},
    packages=[
        'kizuna.api',
        'kizuna.support',
        'kizuna.web',
        'kizuna.worker',
    ],
    tests_require=[
        'pytest'
    ],
    install_requires=REQUIRED
)
