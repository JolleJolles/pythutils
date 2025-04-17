#!/usr/bin/env python
# Copyright (c) 2018 - 2025 Jolle Jolles <j.w.jolles@gmail.com>
# Licensed under the Apache License, Version 2.0

from setuptools import setup, find_packages

# Load version info from pythutils/__version__.py
version = {}
with open("pythutils/__version__.py") as f:
    exec(f.read(), version)

DESCRIPTION = "pythutils: a collection of utility functions for Python"
DISTNAME = "pythutils"
MAINTAINER = "Jolle Jolles"
MAINTAINER_EMAIL = "j.w.jolles@gmail.com"
URL = "https://github.com/JolleJolles"
DOWNLOAD_URL = "https://github.com/JolleJolles/pythutils/archive/refs/tags/" + version["__version__"] + ".tar.gz"

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version=version["__version__"],
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=URL,
        download_url=DOWNLOAD_URL,
        license="Apache-2.0",
        platforms=["Windows", "Linux", "Mac OS-X"],
        packages=find_packages(),  # in case you add submodules later
        include_package_data=True,
        install_requires=[
            "numpy",
            "pyyaml",
            "objsize",
            "seaborn",
        ],
        classifiers=[
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Scientific/Engineering :: Visualization",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
        ],
    )
