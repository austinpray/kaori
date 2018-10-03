python-slacktools
=================

A toolbelt for working with the various `Slack APIs`_ in python.

|Documentation Status| |Build Status| |Code Coverage| |PyPI - Version| |PyPI - Python Version|

.. |Build Status| image:: https://travis-ci.com/austinpray/python-slacktools.svg?branch=master
    :target: https://travis-ci.com/austinpray/python-slacktools
.. |Documentation Status| image:: https://readthedocs.org/projects/python-slacktools/badge/?version=latest
    :target: https://python-slacktools.readthedocs.io/en/latest/?badge=latest
.. |PyPI - Version| image:: https://badge.fury.io/py/slacktools.svg
    :target: https://pypi.org/project/slacktools/
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/Django.svg
    :target: https://pypi.org/project/slacktools/
.. |Code Coverage| image:: https://codecov.io/gh/austinpray/python-slacktools/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/austinpray/python-slacktools


Install
-------

Install slacktools with `PyPI <https://pypi.python.org/pypi>`_

.. code-block:: bash

    pip install slacktools

This library is tested against Python 3.4+. `Open an issue`__ if you need this library to work on an older version.

__ https://github.com/austinpray/python-slacktools/issues/new

Features
--------

- `Authorization utils`_ to verify ``X-Slack-Signature``
- `Message text utils`_ to do things like:
    - Format slack control sequences like ``<@USERIDXX>`` and ``<text|url>``
      with proper escaping
    - Extract mentions and grab user ids from mentions
    - Properly escape message text
- `Message sending functions`_ with partial application to reduce boilerplate
  and improve testability
- `Silly stuff`_

Check out `the docs`_ for more info and `API documentation`_.

Tests
-----

Running the tests is simple enough:

.. code-block:: bash

    python setup.py test

Or just ``pytest`` will do the trick. This will run the tests in the ``tests/``
directory as well as as bunch of docstring tests in the ``src/`` directory.

The Makefile also has some good test commands that will spin up a docker container:

- ``make test`` will run the tests in python 3.7.
- ``make test-all`` will run a series of tests from python 3.7 down to 3.4.
- ``make test-{{PY_VERSION}}`` where ``PY_VERSION`` can be `any tagged version
  of the official python docker image`__ will run tests under that python
  version. Ex: ``make test-3.5`` will run under Python 3.5.

__ https://hub.docker.com/_/python/

Roadmap
-------

- Wider python support? This lib only `supports python 3 <.travis.yml>`_ right
  now. However, if someone needs it, I can add python 2 compatibility.
- Friendly message builder API?
- Build deep links into clients

In the Wild
-----------

`austinpray/kizuna`_ is a silly chatbot that `uses this library <https://github.com/austinpray/kizuna/tree/master/vendor/python-slacktools>`_.


.. _Slack APIs: https://api.slack.com/
.. _Slack: https://api.slack.com/
.. _the docs: https://python-slacktools.readthedocs.io
.. _API documentation: https://python-slacktools.readthedocs.io/en/latest/api.html

.. _Authorization utils: https://python-slacktools.readthedocs.io/en/latest/api.html#module-slacktools.authorization
.. _Message text utils: https://python-slacktools.readthedocs.io/en/latest/api.html#module-slacktools.message
.. _Message sending functions: https://python-slacktools.readthedocs.io/en/latest/api.html#module-slacktools.chat
.. _Silly stuff: https://python-slacktools.readthedocs.io/en/latest/api.html#module-slacktools.arguments
.. _austinpray/kizuna: https://github.com/austinpray/kizuna
