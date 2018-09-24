#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import glob

gevent_deps = [
    'gevent',
    'watchdog-gevent',
]

gunicorn_deps = [
    *gevent_deps,
    'gunicorn',
]

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
    data_files=[('kizuna_static', glob.glob('static/**/*'))],
    tests_require=[
        'pytest'
    ],
    install_requires=[
        'SQLAlchemy',
        'alembic',
        'arrow',
        'backoff',
        'boto3',
        'cryptography',
        'psycopg2',
        'raven[flask]',
        'requests',
        'slackclient',
        'slacktools',
        'ujson',
    ],
    extras_require={
        'web': [
            'Flask',
            *gunicorn_deps,
        ],
        'api': [
            'dramatiq[rabbitmq]',
            'falcon',
            *gunicorn_deps,
        ],
        'worker': [
            'dramatiq[rabbitmq, watch]',
            'graphviz',
            'palettable',
            'spacy',
            *gevent_deps,
        ]
    }
)
