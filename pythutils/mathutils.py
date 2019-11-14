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

from __future__ import division

import numpy as np

def uneven(value):

    """Returns the closest uneven value equal to or lower than provided"""

    if value == 0:
        newvalue = 1
    else:
        newvalue = value -1 if value % 2 == 0 else value

    return newvalue


def closenr(n, m) :

    """Find the number closest to n and divisible by m"""

    q = int(n / m)
    n1 = m * q
    if((n * m) > 0) :
        n2 = (m * (q + 1))
    else :
        n2 = (m * (q - 1))

    if (abs(n - n1) < abs(n - n2)) :
        return n1

    return n2


def seqcount(start, stop, steplength):

    """
    Returns a sequence of numbers between a start and stop value with a
    certain steplength
    """

    step = (stop - start) / length
    step = int(np.ceil(step))
    sequence = range(start, stop, step)

    return sequence


def maxsteps(value, maxval = 500):

    """
    Returns the maximum number of steps and stepsize for a value that may be
    divided up to a maximum value, all being rounded value. For example, if one
    wants to get the maximum number of steps to get to a value of 100 where it
    can be maximally divided 7 times, it will return nsteps=5, stepsize=20.
    """

    valrange = [value-3,value-2,value-1,value]
    nsteps = 1
    for val in valrange:
        for _,n in enumerate(reversed(list(range(1, maxval)))):
            if val % n == 0:
                if n > nsteps:
                    nsteps = int(n)
                    stepsize = int(val/nsteps)
                break

    return(nsteps, stepsize)


def get_weights(w = 1.7, length = 20):

    """Returns a list of weights, based on quadratic function"""

    return [w**i for i in range(length, 0, -1)]


def points_to_vec(pt1, pt2, flip = False):

    """
    Converts the coordinate of two points (pt1 > pt2) to a vector

    flip: bool, default = False
        If the coordinate system should be flipped such that higher y-coords
        are lower (e.g. needed when working with images in opencv).
    """

    vx = pt2[0] - pt1[0]
    vy = pt1[1] - pt2[1] if flip else pt2[1] - pt1[1]

    return vx, vy


def angle_to_vec(angle):

    """
    Converts an angle in degrees to a vector. Uses a coordinate system that
    points north and ranges from -180 to 180 degrees.
    """

    vx = np.round(np.sin(np.radians(angle)), 3)
    vy = np.round(np.cos(np.radians(angle)), 3)

    return vx, vy


def points_to_angle(pt1, pt2 = None, flip = False):

    """
    Returns the angle of a vector from the origin to a single point or the angle
    between two points. Uses a coordinate system that points north and ranges
    from -180 to 180 degrees.

    flip: bool, default = False
        If the coordinate system should be flipped such that higher y-coords
        are lower (e.g. needed when working with images in opencv).
    """

    vx, vy = pt1 if pt2 is None else points_to_vec(pt1, pt2, flip)
    angle = np.round(np.arctan2(vx, vy) * 180 / np.pi,2)

    return angle


def points_to_dist(pt1, pt2):

    """Computes the distance between two points"""

    if None in pt1 or None in pt2:
        dist = None
    else:
        vx, vy = points_to_vec(pt1, pt2)
        dist = np.linalg.norm([(vx, vy)])

    return dist


def diff_series(series, period = 1):

    """Shifts a pandas series upwards with a given period"""

    series2 = series.shift(periods = -period)

    return series2 - series


def dist_to_segment(pt, segment):

    """
    Calculates the distance between a point and a non-infinite line segment

    Explanation
    ----------
    To calculate the closest distance to a line segment, we first need to check
    if the point projects onto the line segment.  If it does, then we calculate
    the orthogonal distance from the point to the line. If the point does not
    project to the line segment, we calculate the distance to both endpoints
    and take the shortest distance.

    Input
    ----------
    point : tuple of the point's coordinates
    line : tuple of segment endpoints' coordinates

    Returns
    -------
    dist : minimum distance to the end point on the line
    coords : the relative x and y coordinates to the line
    """

    # unit vector
    segment = np.array(segment)
    uline = segment[1] - segment[0]
    norm_uline = uline / np.linalg.norm(uline)

    # compute the perpendicular distance to the theoretical infinite line
    dott_product = np.cross(segment[1] - segment[0], segment[0] - pt)
    dist_infline = (np.linalg.norm(dott_product / np.linalg.norm(uline)))
    diff = (norm_uline[0] * (pt[0] - segment[0][0])) + \
           (norm_uline[1] * (pt[1] - segment[0][1]))
    x_seg = np.round((norm_uline[0] * diff) + segment[0][0])
    y_seg = np.round((norm_uline[1] * diff) + segment[0][1])

    linept1dis = np.linalg.norm(segment[0] - pt)
    linept2dis = np.linalg.norm(segment[1] - pt)
    endpoint_dist = min(linept1dis, linept2dis)

    # decide if the intersection point falls on the line segment
    lp1_x = line[0][0]
    lp1_y = line[0][1]
    lp2_x = line[1][0]
    lp2_y = line[1][1]
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y

    if is_betw_x and is_betw_y:
        dist = dist_infline
        coords = (x_seg, y_seg)
    else:
        # if not, then return the minimum distance to the segment endpoints
        dist = endpoint_dist
        coords = (line[0][0],line[0][1]) if linept1dis<=linept2dis else (line[1][0],line[1][1])

    return dist, coords
