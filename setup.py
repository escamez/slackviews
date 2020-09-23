#!/usr/bin/env python
#
# author: aech22@gmail.com
# Copyright (c) 2020 Agustin Escamez
#

from setuptools import setup, find_packages

__author__ = 'agutin.escamezchimeno@telefonica.com'


def _read_file(filename, lines=True, non_empty=False):
    content = open(filename, 'r').read()
    if lines:
        _lines = [line.rstrip(' ') for line in content.split('\n')]
        if non_empty:
            _lines = list(filter(lambda l: l != '', _lines))
        return _lines
    return content


def _version():
    return _read_file('VERSION', lines=True, non_empty=True)[0].rstrip(' ')


setup(
    name='slackviews',
    version=_version(),
    description='Project with a library to generate Slack views from code, using builder pattern',
    long_description_content_type='text/markdown',
    long_description=_read_file('DESCRIPTION.md', lines=False),
    author='Agustin Escamez',
    author_email='aech22@gmail.com',
    url='https://github.com/escamez/slackviews',
    download_url=f'https://github.com/escamez/slackviews/archive/v{_version()}.tar.gz',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=_read_file('KEYWORDS', non_empty=True),
    install_requires=[],
    classifiers=_read_file('CLASSIFIERS', non_empty=True),
    python_requires='>=3.6'
)
