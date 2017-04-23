#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

try:
    with open('BUILD_NUMBER') as f:
        BUILD_NUMBER = int(f.read())
except:
    BUILD_NUMBER = 0


setup(
    name='bg-test',
    version='0.1.%d' % BUILD_NUMBER,
    description='bg_test',
    author='Sergey Pikhovkin',
    author_email='s@pikhovkin.ru',
    url='https://pikhovkin.ru',
    packages=find_packages(exclude=('project',)),
    include_package_data=True,
    install_requires=[
        'Django<1.12',
    ],
)
