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
        import yaml
    except ImportError:
        install_requires.append('pyyaml')
    try:
        import pandas
    except ImportError:
        print("pandas is not installed. Doing so will take considerable time.",end="")
        print("Please install manually when required: pip install pandas")
        #install_requires.append('pandas')
    try:
        import matplotlib
    except ImportError:
        print("Matplotlib is not installed. Please install manually when",end="")
        print("required: pip install matplotlib")
        #install_requires.append('matplotlib')
    try:
        import cv2
    except ImportError:
        print("OpenCV is not installed. Doing so will take considerable time,",end="")
        print("especially on the RPi. Please follow the guidelines for installing",end="")
        print("manually on the mac here: https://git.io/fpyvq")

    return install_requires

install_requires = check_dependencies()

setup(name='animlab',
      author='Jolle Jolles',
      author_email='j.w.jolles@gmail.com',
      description='AnimLab: Sophisticated computational tools for studying animal behaviour',
      long_description=readme,
      url='http://jollejolles.com',
      download_url='https://github.com/JolleJolles/animlab.git',
      version="0.0.5",
      license="MIT",
      install_requires=install_requires,
      packages=['animlab'])
