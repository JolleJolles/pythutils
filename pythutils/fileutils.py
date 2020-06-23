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


def move(file, newdir):

    """Moves a file to new location"""

    if not os.path.isfile(file):
        raise OSError("Provided file does not exist..")
    newdir = os.getcwd()+"/"+newdir if os.path.split(newdir)[0]=="" else newdir
    if not os.path.isdir(newdir):
        raise OSError("Provided newdir is no directory..")

    path, filename = os.path.split(file)
    print(path, filename)
    if path == "":
        path = os.getcwd()
    os.rename(path+"/"+filename, newdir+"/"+filename)


def listfiles(dir = ".", type = "", keepdir = False, keepext = True,
              nested = False):

    """
    Returns a list of (nested) files or directories

    filedir: str; default="."
    filetype: str or tuple of strings; default=""
        Filetype for the files to be listed. If filetype is dir, it will return
    keepdir: bool; default=False
        If the original directory should be kept as part of the filename
    keepext: bool; defaul=True
        If the file extension should be kept in the filenames
    nested: bool; default=False
        If all nested files should be listed
    """

    if nested:
        outlist = []
        for root, dirs, files in os.walk(dir):
             for file in files:
                if file.endswith(type):
                    if keepdir:
                        outlist.append(os.path.join(root, file))
                    else:
                        outlist.append(file)

    else:
        if type == "dir":
            outlist = [i for i in os.listdir(dir) if os.path.isdir(os.path.join(dir, i))]

        else:
            outlist = [each for each in os.listdir(dir) if each.endswith(type)]
            outlist = [i for i in outlist if not i.startswith('.')]

        if keepdir:
            outlist = [filedir + "/" + i  for i in outlist]

    outlist = sorted(outlist)

    if not keepext:
        outlist = [os.path.splitext(file)[0] for file in outlist]

    return outlist


def filechecker(indir = "", outdir = "", move = True, type=".h264",
                sleeptime = 2, function = None, functionparams = ("file")):

        """
        Repeatedly checks a directory for (new) files

        Parameters
        ===========
        indir : str, default = ""
            Directory with original files to monitor
        outdir : str, default = ""
            Directory with new files to monitor
        type : str, default = ".h264"
            The type of file to monitor
        sleeptime : int, default = 2
            Time in seconds between subsequent checks of file folder
        function :
            function to use with the files to check
        functionparams :
            parameters for the function to use
        """

        global interrupted
        interrupted = False
        def keythread():
            global interrupted
            input()
            interrupted = True
        Thread(target=keythread).start()

        if function is None:
            raise Inputerror("No function is provided")
        indir = os.getcwd() if indir == "" else indir
        if not os.path.exists(indir):
            raise OSError("in-directory does not exist..")
        outdir = indir if outdir == "" else outdir
        if not os.path.exists(outdir):
            raise OSError("out-directory does not exist..")

        rootdir = os.getcwd()
        os.chdir(indir)

        while not interrupted:
            files = listfiles(indir, type, keepdir = False)
            if not move:
                old = listfiles(indir, type, keepext = False)
                new = listfiles(outdir, type, keepext = False)
                files = [files[i] for i,file in enumerate(old) if file not in new]
            for file in files:
                if "file" == functionparams:
                    function(file)
                elif "file" in functionparams:
                    function(file, *functionparams[1:])
                else:
                    function(*functionparams)

            lineprint("No files found, rechecking in "+str(sleeptime)+"s..")
            time.sleep(sleeptime)

        os.chdir(rootdir)
        lineprint("Filechecking stopped..")


def commonpref(pathlist = None, remove = False):

    """Given a list of paths, returns the longest common leading component"""

    if pathlist is None: return ""
    s1 = min(pathlist)
    s2 = max(pathlist)
    for i, c in enumerate(s1):
        if c != s2[i]:
            commcomp = s1[:i]
            break

    if remove:
        for each in range(len(pathlist)):
            pathlist[each] = pathlist[each].split(commcomp, 1)[-1]
        return pathlist

    else:
        return commcomp


def get_ext(filename):

    """Returns file extension in lower case"""

    return os.path.splitext(str(filename))[-1].lower()


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
    filename, ext = os.path.splitext(filename)
    names = [x for x in os.listdir(dirname) if x.startswith(filename)]
    names = [x for x in names if os.path.splitext(x)[1]==ext]

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
