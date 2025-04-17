#!/usr/bin/env python
# Copyright (c) 2018 - 2025 Jolle Jolles <j.w.jolles@gmail.com>
# Licensed under the Apache License, Version 2.0

import pandas as pd
import numpy as np

def _list_to_coords(list):

    coords = [(int(i),int(j)) for i,j in list if i==i]
    loclist = [c for c,i in enumerate(list) if i[0] == i[0]]

    return coords, loclist


def create_emptydf(cols = ["x","y","fx","fy"], ids = [1], first = 1, last = None):

    """
    Creates an emtpy pandas dataframe, aimed to hold coordinate data

    cols : a list of columns
    ids : a list of animal ids
    first : start frame
    last : last frame
    """

    try:
        framerange = range(first, last + 1)
    except TypeError:
        raise TypeError("No last value provided..")

    colnames = ["frame","id"] + cols
    emptycols = list(np.repeat(np.nan, len(cols)))

    for i, id in enumerate(ids):
        sub = pd.DataFrame([[frame, id] + emptycols for frame in framerange],
              columns = colnames)
        data = sub if i == 0 else pd.concat([data, sub])

    data = data.sort_values(["frame"])
    data.index = range(0, data.index.size, 1)

    return data


def pd_to_coords(pdat, loc = None, array = False, columns = ["x","y"],
                 multiplier = 1):

    """
    Returns either a single coordinate of integers or a list or an array of
    arrays with coordinates with a list of frames
    """

    if loc != None:
        coords = _list_to_coords([list(pdat.loc[loc, columns])])[0]
        if len(coords) == 0:
            return None
        else:
            c = coords[0]
            return (int(c[0]*multiplier),int(c[1]*multiplier))

    else:
        coords, loclist = _list_to_coords(list(zip(pdat[columns[0]],
                                                   pdat[columns[1]])))
        framelist = [pdat.loc[i,"frame"] for i in loclist]
        coords = [(int(c[0]*multiplier),int(c[1]*multiplier)) for c in coords]
        if array:
            coords = [[[i] for i in coords]]
            coords = np.array(coords, np.int32).reshape((-1,1,2))

        return coords, framelist


def dfchange(df1, df2):

    """Determines the differences between two pandas dataframes"""

    dfchanges = df2.loc[df2[~df2.isin(df1)].dropna(how="all").index,]
    nchanges = dfchanges.shape[0]

    return dfchanges, nchanges


def to_query(cols, vals):

    """Returns a query from a list of columns and values"""

    vals = ["'"+val+"'" if isinstance(val,str) else val for val in vals]
    query = ['{} == {}'.format(cols[i],vals[i]) for i,_ in enumerate(cols)]
    query = ' and '.join(query)

    return query


def contour_to_tuple(contour):

    """Convert contour to tuple"""

    conttuple = [(row[0][0], row[0][1]) for row_idx, row in enumerate(contour)]

    return conttuple
