#! /usr/bin/env python
# Copyright (c) 2018 - 2019 Jolle Jolles <j.w.jolles@gmail.com>
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

from setuptools import setup, find_packages
import sys

exec(open("pythutils/__version__.py").read())

DESCRIPTION = """pythutils: a collection of utility functions for Python"""

DISTNAME = "pythutils"
MAINTAINER = "Jolle Jolles"
MAINTAINER_EMAIL = "j.w.jolles@gmail.com"
URL = "https://github.com/JolleJolles"
DOWNLOAD_URL = "https://github.com/JolleJolles/pythutils/archive/1.3.5.tar.gz"

with open("README.md") as f:
    readme = f.read()


if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=readme,
          long_description_content_type="text/markdown",
          url=URL,
          download_url=DOWNLOAD_URL,
          version=__version__,
          license="License :: OSI Approved :: Apache Software License",
          platforms=["Windows", "Linux", "Mac OS-X"],
          packages=["pythutils"],
          install_requires=[
                     "numpy==1.16.5; python_version>='2' and python_version<'3'",
                     "numpy; python_version>='3'",
                     "pandas==0.24.2; python_version>='2' and python_version<'3'",
                     "pandas; python_version>='3'",
                     "pyyaml",
                     "h5py"],
          classifiers=[
                     "Intended Audience :: Science/Research",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: Apache Software License",
                     "Topic :: Scientific/Engineering :: Visualization",
                     "Topic :: Scientific/Engineering :: Image Recognition",
                     "Topic :: Scientific/Engineering :: Information Analysis",
                     "Topic :: Multimedia :: Video",
                     "Operating System :: POSIX",
                     "Operating System :: Unix",
                     "Operating System :: MacOS"],
          )
