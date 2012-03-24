#!/usr/bin/env python
#-*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

name = "comet"
version = "0.1"

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version=version,
    description="彗星",
    long_description=read('README.md'),
    keywords="",
    author="",
    author_email='',
    url='',
    license='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'mysql-python',
        'redis',
        'httplib2',
        ],
    entry_points="""
    [console_scripts]
    start = app:run
    """,
)
