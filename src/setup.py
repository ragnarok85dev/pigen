# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from _version import __version__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    the_license = f.read()

setup(
    name='pigen',
    version=__version__,
    description='Python Interpreter of GENealogical data',
    long_description=readme,
    author='Giacomo Ricca',
    author_email='giacomo.ricca@gmail.com',
    url='https://github.com/ragnarok85dev/pigen',
    license=the_license,
    packages=find_packages(exclude=('tests', 'docs'))
)