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

from __future__ import print_function

import cv2
import numpy as np

from pythutils.mathutils import sort_twoPoint


def textdims(text, size, thickness = 1):

    """Get uniform text dimensions for printing text with opencv"""

    tw, th = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, size, thickness)[0]

    topy = size*1 if any(x in ["i","j"] for x in text) else 0
    boty = size*2 if any(x in "Q" for x in text) else 0
    boty = size*7 if any(x in ["g","j","y","p","q"] for x in text) else boty

    return (tw, th), topy, boty


class mouse_events:

    """Stores a series of coordinates related to mouse events"""

    def __init__(self):

        self.pos = (0,0)
        self.pts = []
        self.posDown = None
        self.posUp = None
        self.twoPoint = None
        self.drawing = False

    def draw(self, event, x, y, flags, param):

        if event == cv2.EVENT_MOUSEMOVE:
            self.pos = (x,y)

        if event == cv2.EVENT_LBUTTONDOWN:
            self.posDown = (x,y)
            self.pts.append((x,y))
            self.posUp = None

        if event == cv2.EVENT_LBUTTONUP:
            self.posUp = (x,y)
            self.twoPoint = sort_twoPoint((self.pts[-1], self.posUp))
            self.posDown = None

        self.drawing = True


def namedcols(colname = None, printlist = False, BRG = True):

    """Acquire RGB/BRG colors from a color name"""

    collist = {'black': (0, 0, 0),
             'navy': (0, 0, 128),
             'navyblue': (0, 0, 128),
             'darkblue': (0, 0, 139),
             'mediumblue': (0, 0, 205),
             'blue': (0, 0, 255),
             'darkgreen': (0, 100, 0),
             'green': (0, 128, 0),
             'darkcyan': (0, 139, 139),
             'deepskyblue': (0, 191, 255),
             'darkturquoise': (0, 206, 209),
             'mediumspringgreen': (0, 250, 154),
             'lime': (0, 255, 0),
             'springgreen': (0, 255, 127),
             'cyan': (0, 255, 255),
             'aqua': (0, 255, 255),
             'midnightblue': (25, 25, 112),
             'dodgerblue': (30, 144, 255),
             'lightseagreen': (32, 178, 170),
             'forestgreen': (34, 139, 34),
             'seagreen': (46, 139, 87),
             'darkslategray': (47, 79, 79),
             'darkslategrey': (47, 79, 79),
             'limegreen': (50, 205, 50),
             'mediumseagreen': (60, 179, 113),
             'turquoise': (64, 224, 208),
             'royalblue': (65, 105, 225),
             'steelblue': (70, 130, 180),
             'darkslateblue': (72, 61, 139),
             'mediumturquoise': (72, 209, 204),
             'indigo': (75, 0, 130),
             'darkolivegreen': (85, 107, 47),
             'cadetblue': (95, 158, 160),
             'cornflowerblue': (100, 149, 237),
             'mediumaquamarine': (102, 205, 170),
             'dimgray': (105, 105, 105),
             'dimgrey': (105, 105, 105),
             'slateblue': (106, 90, 205),
             'olivedrab': (107, 142, 35),
             'slategray': (112, 128, 144),
             'slategrey': (112, 128, 144),
             'lightslategray': (119, 136, 153),
             'lightslategrey': (119, 136, 153),
             'mediumslateblue': (123, 104, 238),
             'lawngreen': (124, 252, 0),
             'chartreuse': (127, 255, 0),
             'aquamarine': (127, 255, 212),
             'maroon': (128, 0, 0),
             'purple': (128, 0, 128),
             'olive': (128, 128, 0),
             'gray': (128, 128, 128),
             'grey': (128, 128, 128),
             'lightslateblue': (132, 112, 255),
             'skyblue': (135, 206, 235),
             'lightskyblue': (135, 206, 250),
             'blueviolet': (138, 43, 226),
             'darkred': (139, 0, 0),
             'darkmagenta': (139, 0, 139),
             'saddlebrown': (139, 69, 19),
             'darkseagreen': (143, 188, 143),
             'lightgreen': (144, 238, 144),
             'mediumpurple': (147, 112, 219),
             'darkviolet': (148, 0, 211),
             'palegreen': (152, 251, 152),
             'darkorchid': (153, 50, 204),
             'yellowgreen': (154, 205, 50),
             'sienna': (160, 82, 45),
             'brown': (165, 42, 42),
             'darkgray': (169, 169, 169),
             'darkgrey': (169, 169, 169),
             'lightblue': (173, 216, 230),
             'greenyellow': (173, 255, 47),
             'paleturquoise': (175, 238, 238),
             'lightsteelblue': (176, 196, 222),
             'powderblue': (176, 224, 230),
             'firebrick': (178, 34, 34),
             'darkgoldenrod': (184, 134, 11),
             'mediumorchid': (186, 85, 211),
             'rosybrown': (188, 143, 143),
             'darkkhaki': (189, 183, 107),
             'silver': (192, 192, 192),
             'mediumvioletred': (199, 21, 133),
             'indianred': (205, 92, 92),
             'peru': (205, 133, 63),
             'violetred': (208, 32, 144),
             'chocolate': (210, 105, 30),
             'tan': (210, 180, 140),
             'lightgray': (211, 211, 211),
             'lightgrey': (211, 211, 211),
             'thistle': (216, 191, 216),
             'orchid': (218, 112, 214),
             'goldenrod': (218, 165, 32),
             'palevioletred': (219, 112, 147),
             'crimson': (220, 20, 60),
             'gainsboro': (220, 220, 220),
             'plum': (221, 160, 221),
             'burlywood': (222, 184, 135),
             'lightcyan': (224, 255, 255),
             'lavender': (230, 230, 250),
             'darksalmon': (233, 150, 122),
             'violet': (238, 130, 238),
             'lightgoldenrod': (238, 221, 130),
             'palegoldenrod': (238, 232, 170),
             'lightcoral': (240, 128, 128),
             'khaki': (240, 230, 140),
             'aliceblue': (240, 248, 255),
             'honeydew': (240, 255, 240),
             'azure': (240, 255, 255),
             'sandybrown': (244, 164, 96),
             'wheat': (245, 222, 179),
             'beige': (245, 245, 220),
             'whitesmoke': (245, 245, 245),
             'mintcream': (245, 255, 250),
             'ghostwhite': (248, 248, 255),
             'salmon': (250, 128, 114),
             'antiquewhite': (250, 235, 215),
             'linen': (250, 240, 230),
             'lightgoldenrodyellow': (250, 250, 210),
             'oldlace': (253, 245, 230),
             'red': (255, 0, 0),
             'magenta': (255, 0, 255),
             'fuchsia': (255, 0, 255),
             'deeppink': (255, 20, 147),
             'orangered': (255, 69, 0),
             'tomato': (255, 99, 71),
             'hotpink': (255, 105, 180),
             'coral': (255, 127, 80),
             'darkorange': (255, 140, 0),
             'lightsalmon': (255, 160, 122),
             'orange': (255, 165, 0),
             'lightpink': (255, 182, 193),
             'pink': (255, 192, 203),
             'gold': (255, 215, 0),
             'peachpuff': (255, 218, 185),
             'navajowhite': (255, 222, 173),
             'moccasin': (255, 228, 181),
             'bisque': (255, 228, 196),
             'mistyrose': (255, 228, 225),
             'blanchedalmond': (255, 235, 205),
             'papayawhip': (255, 239, 213),
             'lavenderblush': (255, 240, 245),
             'seashell': (255, 245, 238),
             'cornsilk': (255, 248, 220),
             'lemonchiffon': (255, 250, 205),
             'floralwhite': (255, 250, 240),
             'snow': (255, 250, 250),
             'yellow': (255, 255, 0),
             'lightyellow': (255, 255, 224),
             'ivory': (255, 255, 240),
             'white': (255, 255, 255)}

    if printlist:
        print(collist)
    elif colname not in collist:
        print("colname does not exist..")
    else:
        col = collist[colname]
        col = (col[2],col[1],col[0]) if BRG else col
        return col


def get_spaced_colors(colnr):

    """Gets a specified nr of colors, equally spaced on the color spectrum"""

    maxval = 255**3
    interval = int(maxval/(colnr+0.5))
    colshex = [hex(I)[2:].zfill(6) for I in list(range(0, maxval, interval))]
    colsrgb = [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colshex]
    colsrgb = colrgb[1:]

    return colsrgb


def draw_text(img, text, loc = (0, 0), size = 1, col = "black", margin = 5,
              thickness = 1, bgcol = None, shadow = False):

    """
    Draw text on opencv image

    img : an image array
    text : the text to draw
    loc : the location of the text relative to topleft
    size : the size of the text
    col : the color of the text
    margin : the margin of the text
    thickness : the weight of the text
    bgcol : the potential background color of the text

    """

    col = namedcols(col)
    (tw, th), topy, boty = textdims(text, size)
    topy = topy + int(thickness/2)
    boty += int(thickness/2)

    if bgcol is not None:
        bgcol = namedcols(bgcol)
        topleftout = (loc[0], loc[1])
        botrightx = loc[0] + margin + tw + margin + 1
        botrighty = loc[1] + margin + th + topy + boty + margin + 1
        botrightout = (botrightx, botrighty)
        cv2.rectangle(img, topleftout, botrightout, bgcol, -1)

    botlefin = (int(loc[0]+margin), int(loc[1]+margin+th+topy))
    if shadow:
        cv2.putText(img, text, botlefin, cv2.FONT_HERSHEY_SIMPLEX, size,
                    (0,0,0), int(thickness*3), cv2.LINE_AA)
    cv2.putText(img, text, botlefin, cv2.FONT_HERSHEY_SIMPLEX, size,
                col, thickness, cv2.LINE_AA)


def draw_cross(img, pt1 = (1,1), pt2 = None, col = "white", thickness = 2):

    """Draws a cross"""

    pt2 = (img.shape[1],img.shape[0]) if pt2 == None else pt2
    cv2.line(img, pt1, (pt2[0], pt2[1]), namedcols(col), thickness)
    cv2.line(img, (pt2[0], pt1[0]), (pt1[1], pt2[1]), namedcols(col), thickness)


def draw_hcross(img, col="white", thickness=2, style="dashed"):

    """Draws a horizontal cross"""

    midTop = (int(img.shape[1]/2),1)
    midBot = (int(img.shape[1]/2),img.shape[0])
    midLeft = (1,int(img.shape[0]/2))
    midRight = (img.shape[1],int(img.shape[0]/2))
    draw_sliced_line(img, midTop, midBot, col, thickness, style)
    draw_sliced_line(img, midLeft, midRight, col, thickness, style)


def draw_crosshair(img, pt, radius = 5, col = "white"):

    """Draws a crosshair"""

    hline = (pt[0] - radius, pt[1]), (pt[0] + radius, pt[1])
    tline = (pt[0], pt[1] - radius), (pt[0], pt[1] + radius)
    cv2.line(img, hline[0], hline[1], namedcols(col), 1)
    cv2.line(img, tline[0], tline[1], namedcols(col), 1)


def draw_rectangle(img, pointer, rect, drawing = False, col = "red"):

    """Draws a rectangle with option to show it dynamically"""

    if drawing:
        cv2.rectangle(img, rect[0], pointer, namedcols(col), 2)

    else:
        cv2.rectangle(img, rect[0], rect[1], namedcols(col), 2)


def draw_bicircles(img, pt, resizeval = 1, col1 = "black", col2 = "white",
                   minsize = 3, maxsize = 15, stepsize = 3):

    """Draws a range of increasing bi-colored circles"""

    sizes = list(reversed(range(minsize, maxsize+stepsize, stepsize)))
    for i, size in enumerate(sizes):
        col = namedcols(col1) if i%2==0 else namedcols(col2)
        cv2.circle(img, pt, 0, col, int(size*resizeval))


def draw_sliced_line(img, pt1, pt2, color, thickness = 1, style = "dotted",
                     gap = 5):

    """Draw a dashed or dotted line on an image"""

    col = namedcols(color)
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []

    for i in np.arange(0, dist, gap):
        r = i/dist
        x = int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y = int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        pts.append((x,y))

    if style == "dotted":
        for pt in pts:
            cv2.circle(img, pt, thickness, col, -1)

    if style == "dashed":
        s = e = pts[0]
        for i,pt in enumerate(pts):
            s = e
            e = pt
            if i%2 == 1:
                cv2.line(img, s, e, col, thickness)


def draw_traj(img, coordlist = [], color = "green", thick_min = 8,
              thick_max = 13, opacity = 0.5):

    """Draws a semi-transparent polyline with decreasing width on an image"""

    col = namedcols(color)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = img2.copy()

    thicklist = np.linspace(thick_min, thick_max, len(coordlist))
    thicklist = (thicklist**4 / thick_max**4) * thick_max

    for i in list(range(1, (len(coordlist) - 1))):
        thickness = int(thicklist[i])
        if coordlist[i] != coordlist[i] or coordlist[i-1] != coordlist[i-1]:
            continue
        elif None in sum((coordlist[i], coordlist[i-1]),()):
            continue

        cv2.line(mask, coordlist[i], coordlist[i-1], col, thickness)

    cv2.addWeighted(mask, opacity, img2, 1-opacity, 0, img)
