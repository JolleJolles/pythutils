
# coding: utf-8

# In[ ]:

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
import numpy as np
import pandas as pd
from matplotlib import colors as mcolors

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
    

def namedcols(colname = None, printlist = False, BRG = True):
    
    collist = [str(i) for i in mcolors.CSS4_COLORS]

    if printlist:
        print collist
    elif colname not in collist:
        print "Colname does not exist.."
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
        print "No right time format provided.."


def listfiles(filedir = ".", filetype = (".mp4", ".mov", ".mjpeg",".jpg"), 
              dirs = False):
    
    """ Extracts and returns either a list of files with a specific 
        extension or a list of directories at a certain location
    """

    if dirs:
        outlist = [i for i in os.listdir(filedir) if os.path.isdir(os.path.join(filedir, i))]
        
    else:
        outlist = [each for each in os.listdir(filedir) if each.endswith(filetype)]
        outlist = [i for i in outlist if not i.startswith('.')]

    outlist = sorted(outlist)
    
    return outlist


def get_ext(filename):
    
    """ Returns file extension in lower case"""
    
    return os.path.splitext(filename)[-1].lower()    


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


def create_emptydf(cols = ["x","y","fx","fy"], cids = [1], first = 1, last = None):
    
    """ Creates an emtpy pandas df with frame and cid columns
        as well as user provided columns for provided frame range
    """
    
    try:
        framerange = range(first, last + 1)
    except TypeError:
        raise TypeError("No last value provided..")
    
    colnames = ["frame","cid"] + cols
    emptycols = list(np.repeat(np.nan, len(cols)))
    
    for i, cid in enumerate(cids):
        sub = pd.DataFrame([[frame, cid] + emptycols for frame in framerange], columns = colnames)
        data = sub if i == 0 else pd.concat([data, sub])
        
    data = data.sort_values(["frame"])
    data.index = range(0, data.index.size, 1)
    
    return data


def dfchange(df1, df2):
        
    dfchanges = df2[~df2.isin(df1)].dropna(how = 'all')
    nchanges = dfchanges.shape[0]

    return dfchanges, nchanges

