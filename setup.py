#! /usr/bin/env python
#
# Copyright (C) 2018 Jolle Jolles <j.w.jolles@gmail.com>

from __future__ import print_function
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

DESCRIPTION = 'AnimLab: Sophisticated computational tools for studying animal behaviour'

def check_dependencies():
    install_requires = []

    try:
        import numpy
    except ImportError:
        install_requires.append('numpy')
    try:
        import yaml
    except ImportError:
        install_requires.append('pyyaml')
    try:
        import pandas
    except ImportError:
        install_requires.append('pandas')
    try:
        import matplotlib
    except ImportError:
        install_requires.append('matplotlib')

    return install_requires

install_requires = check_dependencies()

setup(name='animlab',
      author='Jolle Jolles',
      author_email='j.w.jolles@gmail.com',
      description=DESCRIPTION,
      long_description=readme,
      url='http://jollejolles.com',
      download_url='https://github.com/JolleJolles/animlab.git',
      version="0.0.5",
      license="MIT",
      install_requires=install_requires,
      packages=['animlab'])
