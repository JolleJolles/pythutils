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
import ast
import yaml
import h5py
import pandas

def listfiles(filedir = ".", filetype = "", keepdir = False, nested = False):

    """
    Returns a list of (nested) files or directories

    filedir: str; default="."
    filetype: str or tuple of strings; default=""
        Filetype for the files to be listed. If filetype is dir, it will return
    keepdir: bool; default=False
        If the original directory should be kept as part of the filename
    nested: bool; default=False
        If all nested files should be listed
    """

    if filetype == "dir":
        outlist = [i for i in os.listdir(filedir) if os.path.isdir(os.path.join(filedir, i))]

    elif nested:
        outlist = []
        for root, dirs, files in os.walk(filedir):
             for file in files:
                if file.endswith(filetype):
                    outlist.append(file)

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
    newvalue = ast.literal_eval(str(newvalue))

    return newvalue


def loadh5data(filename, dataset = "data"):

    h5file = h5py.File(filename, 'r')
    dataset = pandas.DataFrame(h5file[dataset][:])
    h5file.close()

    return dataset


def name(filename, ext = "", action = "newfile"):

    """
    Gets the name for a file with required extension, and will either overwrite
    the existing file or generate a new file with a sequence.
    """

    dirname, filename = os.path.split(filename)
    dirname = '.' if dirname == '' else dirname
    filename = os.path.splitext(filename)[0]
    names = [x for x in os.listdir(dirname) if x.startswith(filename)]

    if len(names) == 0 or action == "append":
        return filename+ext

    elif action == "overwrite":
        if os.path.exists(filename+ext):
            os.remove(filename+ext)
        return filename+ext

    elif action == "newfile":
        names = [os.path.splitext(x)[0] for x in names]
        suffixes = [x.replace(filename, '') for x in names]
        suffixes = [int(x[1]) for x in suffixes if x.startswith('_')]
        suffix = 2 if len(suffixes)==0 else max(suffixes)+1
        return '%s_%d%s' % (filename, suffix, ext)
