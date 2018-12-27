#! /usr/bin/env python
#
# Python toolset for the mechanistic study of animal behaviour
# Copyright (c) 2018 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from setuptools import setup, find_packages
from .__version__ import __version__


DESCRIPTION = 'AnimLab: Python toolset for the mechanistic study of animal behaviour'

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
      version=__version__,
      license="MIT",
      install_requires=install_requires,
      packages=['animlab'])
