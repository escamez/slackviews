#!/usr/bin/env python
#
# author: aech22@gmail.com
# Copyright (c) 2020 Agustin Escamez
#

from setuptools import setup, find_packages

__author__ = 'agutin.escamezchimeno@telefonica.com'

setup(
    name='slackviews',
    version='1.0.0',
    description='PProject with a library to generate Slack views from code, using builder pattern',
    long_description=open('README.md').read(),
    author='Agustin Escamez',
    author_email='aech22@gmail.com',
    url='https://github.com/escamez/slackviews.git',
    platforms='Linux',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[line for line in open('requirements.txt', 'r').read().split('\n') if line is not ''],
    classifiers=[line for line in open('CLASSIFIERS', 'r').read().split('\n') if line is not ''],
)
