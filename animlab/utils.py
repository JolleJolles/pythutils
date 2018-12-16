from __future__ import division
from __future__ import print_function

"""
Copyright 2018 Jolle W Jolles <j.w.jolles@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
import datetime
import os
import time
import numpy as np
import pandas as pd
from socket import gethostname
from matplotlib import colors as mcolors
import yaml


def deleteline(n=1):

    for _ in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


def lineprint(text, stamp=True, sameline=False, reset=False, **kwargs):

    global line, label

    line = line if vardefined("line") else ""
    label = label if vardefined("label") else gethostname()
    if not vardefined("label"):
        label = ""

    if "label" in kwargs:
        label = kwargs["label"]

    if stamp:
        text = time.strftime("%H:%M:%S") + " [" + label + "] - " + text

    if sameline:
        if reset:
            line = text
            sys.stdout.write("\r")
            sys.stdout.write(" "*100)
        else:
            text = line + " " + text
        line = "\r" + text
        print(line,end='')
    else:
        line = text
        if line == "":
            print(line,end='')
        else:
            print("\n" + text,end='')


def clock():

    """ Simple running clock that prints on the same line"""

    while True:
        print(datetime.datetime.now().strftime("%H:%M:%S")+"\r")
        time.sleep(1)


def isscript():

    """Determines if session is script or interactive (jupyter)"""

    import __main__ as main
    return hasattr(main, '__file__')


def hide_traceback():

    """ Hides traceback in jupyter when raising errors. Only shows
        error. Only needs to be called at start of script.
    """

    ipython = get_ipython()

    def hide(exc_tuple = None, filename = None, tb_offset = None,
             exception_only = False, running_compiled_code = False):
        etype, value, tb = sys.exc_info()
        element = ipython.InteractiveTB.get_exception_only(etype, value)

        return ipython._showtraceback(etype, value, element)

    ipython.showtraceback = hide


def homedir():

    """ Returns the home directory """

    return os.path.expanduser("~")+"/"


def namedcols(colname = None, printlist = False, BRG = True):

    collist = [str(i) for i in mcolors.CSS4_COLORS]

    if printlist:
        print(collist)
    elif colname not in collist:
        print("Colname does not exist..")
    else:
        col = tuple(int(i*255) for i in mcolors.to_rgb(colname))
        col = (col[2],col[1],col[0]) if BRG else col
        return col


def now(timeformat = "date"):

    """ Returns current date or time """

    if timeformat == "date":
        return datetime.datetime.now().strftime("%y/%m/%d")

    elif timeformat == "time":
        return datetime.datetime.now().strftime("%H:%M:%S")

    else:
        print("No right time format provided..")


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


def loadyml(filename, value = None, add = True):

    """ Loads value from .yml file and returns literal"""

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
    dataset = pd.DataFrame(h5file[dataset][:])
    h5file.close()

    return dataset


def get_ext(filename):

    """ Returns file extension in lower case"""

    return os.path.splitext(filename)[-1].lower()


def name(filename, ext = ".csv", action = "overwrite"):

    """ Returns filename with required extension or for sequence
        returns filename that does not exist already with numeric
        '_x' suffix appended
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


def seqcount(start, stop, length):

    """ Returns a sequence of numbers between two values
        with a certain length
    """

    step = (stop - start) / float(length)
    step = int(np.ceil(step))
    sequence = range(start, stop, step)

    return sequence


def get_weights(w = 1.7, length = 20):

    """ Returns a list of weights, based on quadratic function """

    return [w**i for i in range(length, 0, -1)]


def create_emptydf(cols = ["x","y","fx","fy"], ids = [1], first = 1, last = None):

    """ Creates an emtpy pandas df with frame and cid columns
        as well as user provided columns for provided frame range
    """

    try:
        framerange = range(first, last + 1)
    except TypeError:
        raise TypeError("No last value provided..")

    colnames = ["frame","id"] + cols
    emptycols = list(np.repeat(np.nan, len(cols)))

    for i, id in enumerate(ids):
        sub = pd.DataFrame([[frame, id] + emptycols for frame in framerange], columns = colnames)
        data = sub if i == 0 else pd.concat([data, sub])

    data = data.sort_values(["frame"])
    data.index = range(0, data.index.size, 1)

    return data


def dfchange(df1, df2):

    dfchanges = df2.loc[df2[~df2.isin(df1)].dropna(how="all").index,]
    nchanges = dfchanges.shape[0]

    return dfchanges, nchanges


def vardefined(var):

    return var in [var for var,_ in globals().items()]


def list_to_coords(list):
    coords = [(int(i),int(j)) for i,j in list if i==i]
    loclist = [c for c,i in enumerate(list) if i[0] == i[0]]
    return coords, loclist


def pd_to_coords(pddata, loc = None, array = False, columns = ["x","y"], multiplier = 1):

    '''Returns either a single coordinate of integers or a list or an array
       of arrays with coordinates with a list of frames
    '''

    if loc != None:
        coords = list_to_coords([list(pddata.loc[loc, columns])])[0]
        if len(coords) == 0:
            return None
        else:
            c = coords[0]
            return (int(c[0]*multiplier),int(c[1]*multiplier))

    else:
        coords, loclist = list_to_coords(zip(pddata[columns[0]], pddata[columns[1]]))
        framelist = [pddata.loc[i,"frame"] for i in loclist]
        coords = [(int(c[0]*multiplier),int(c[1]*multiplier)) for c in coords]
        if array:
            coords = [[[i] for i in coords]]
            coords = np.array(coords, np.int32).reshape((-1,1,2))

        return coords, framelist
