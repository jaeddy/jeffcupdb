# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "jeffcupdb"
VERSION = "0.1.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion==2.0.0",
    "swagger-ui-bundle==0.0.2",
    "python_dateutil==2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="JeffCup DB",
    author_email="",
    url="",
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True
)

