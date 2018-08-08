#! /usr/bin/env python
#
# Copyright (C) 2018 Jolle Jolles <j.w.jolles@gmail.com>

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

def check_dependencies():
    install_requires = []

    try:
        import numpy
    except ImportError:
        install_requires.append('numpy')
    try:
        import markdown
    except ImportError:
        install_requires.append('markdown')

    return install_requires

install_requires = check_dependencies()

setup(name='animlab',
      author='Jolle Jolles',
      author_email='j.w.jolles@gmail.com',
      description='AnimLab: Sophisticated computational tools for studying animal behaviour',
      long_description=readme,
      url='http://jollejolles.com',
      download_url='https://github.com/jolleslab/animlab.git',
      version="0.0.3",
      license="MIT",
      install_requires=install_requires,
      packages=find_packages(exclude=('tests', 'docs')))
