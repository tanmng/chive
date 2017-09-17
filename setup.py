#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='chive',
    version='0.0.1',
    description='Coin-Hive Client API',
    author='Tan Nguyen',
    author_email='nmtan.90@gmail.com',
    url='https://github.com/nmtan/chive',
    keywords=['Coin-Hive'],
    classifiers=['License :: OSI Approved :: Apache Software License'],
    packages=find_packages(),
    install_requires=[
        'requests>=2.7.0',
    ]
    extras_require = { }
