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

import os
import yaml
import h5py
import pandas

def listfiles(filedir = ".", filetype = (".mp4", ".mov", ".mjpeg",".jpg"),
              dirs = False, keepdir = False):

    """
    Extracts and returns either a list of files with a specific
    extension or a list of directories at a certain location

    Parameters
    ==========
    filedir: str; default="."
    filetype: str; default=(".mp4", ".mov", ".mjpeg",".jpg")
    dirs: bool; default=False
    keepdir: bool; default=False
    """

    if dirs:
        outlist = [i for i in os.listdir(filedir) if os.path.isdir(os.path.join(filedir, i))]

    else:
        outlist = [each for each in os.listdir(filedir) if each.endswith(filetype)]
        outlist = [i for i in outlist if not i.startswith('.')]

    if keepdir:
        outlist = [filedir + "/" + i  for i in outlist]

    outlist = sorted(outlist)

    return outlist


def get_ext(filename):

    """Returns file extension in lower case"""

    return os.path.splitext(filename)[-1].lower()


def loadyml(filename, value = None, add = True):

    """Loads value from .yml file and returns literal"""

    if os.path.exists(filename):
        with open(filename) as f:
            newvalue = yaml.load(f)
        if value is not None:
            newvalue = newvalue + value if add else value
    else:
        newvalue = value
    newvalue = literal_eval(str(newvalue))

    return newvalue


def loadh5data(filename, dataset = "data"):

    h5file = h5py.File(filename, 'r')
    dataset = pandas.DataFrame(h5file[dataset][:])
    h5file.close()

    return dataset


def name(filename, ext = ".csv", action = "overwrite"):

    """
    Returns filename with required extension or for sequence returns filename
    that does not exist already with numeric '_x' suffix appended.
    """

    dirname, filename = os.path.split(filename)
    dirname = '.' if dirname == '' else dirname
    filename = os.path.splitext(filename)[0]

    if action == "replace":
        if os.path.exists(filename+ext):
            os.remove(filename+ext)
        return filename+ext

    elif action == "append":
        return filename+ext

    elif action == "newfile":
        names = [x for x in os.listdir(dirname) if x.startswith(filename)]
        names = [os.path.splitext(x)[0] for x in names]
        suffixes = [x.replace(filename, '') for x in names]
        suffixes = [int(x[1]) for x in suffixes if x.startswith('_')]
        suffix = 1 if len(suffixes)==0 else max(suffixes)+1
        return '%s_%d%s' % (filename, suffix, ext)
