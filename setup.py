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
        import pandas
    except ImportError:
        install_requires.append('pandas')
    try:
        import matplotlib
    except ImportError:
        install_requires.append('matplotlib')
    try:
        import yaml
    except ImportError:
        install_requires.append('pyyaml')
    try:
        import cv2
    except ImportError:
        install_requires.append('cv2')

    return install_requires

install_requires = check_dependencies()

setup(name='animlab',
      author='Jolle Jolles',
      author_email='j.w.jolles@gmail.com',
      description='AnimLab: Sophisticated computational tools for studying animal behaviour',
      long_description=readme,
      url='http://jollejolles.com',
<<<<<<< HEAD
      download_url='https://github.com/jolleslab/animlab.git',
=======
      download_url='https://github.com/joljols/animlab.git',
>>>>>>> 2d365141846c1be0db9dd011ffcf3b2f49147a10
      version="0.0.5",
      license="MIT",
      install_requires=install_requires,
      packages=['animlab'])
