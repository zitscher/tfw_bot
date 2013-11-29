#!/usr/bin/env python

from setuptools import setup

setup(
    name='tfw_bot',
    version='1',
    description='TFW IRC Bot',
    author='Tobias Cichon',
    author_email='cichon@traum-ferienwohnungen.de',
    url='',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ]
)