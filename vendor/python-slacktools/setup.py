# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os
import re


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


long_description = read('README.rst')


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='slacktools',
      version=find_version('src', 'slacktools', 'version.py'),
      description='Toolbelt for Slack API clients for Web API and RTM API',
      long_description=long_description,
      url='https://github.com/austinpray/python-slacktools',
      author='Austin Pray',
      author_email='austin@austinpray.com',
      license='MIT',
      classifiers=[
          #'Development Status :: 5 - Production/Stable',
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Topic :: Communications :: Chat',
          'Topic :: System :: Networking',
          'Topic :: Office/Business',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      keywords='slack slack-web slack-rtm slacktools chat chatbots bots chatops',
      packages=find_packages(exclude=['docs', 'tests']),
      setup_requires=["pytest-runner"],
      tests_require=["pytest", "pytest-cov"],
      install_requires=[
          "typing ; python_version<'3.5'"
      ])
