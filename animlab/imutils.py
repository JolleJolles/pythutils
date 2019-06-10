#! /usr/bin/env python
#
# Python toolset for the mechanistic study of animal behaviour
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
from __future__ import print_function

import os
import cv2
from animlab.utils import *


def check_media(mediafile):

    ext = get_ext(mediafile)
    vidtypes = [".mov",".mp4",".avi"]
    imgtypes = [".jpg", ".png", ".jpeg", ".bmp"]
    ftype = "vid" if ext in vidtypes else "img" if ext in imgtypes else None
    filedir = os.path.dirname(mediafile)

    assert ftype != None, "File neither Video or image file.."
    if filedir != "":
        assert os.path.isdir(filedir), "File directory does not exist.."
    assert os.path.isfile(mediafile), "File does not exist.."

    if ftype == "vid":
        cap = cv2.VideoCapture(mediafile)
        assert cap.read()[0], "Video source opened but failed to read images.."

    print("Mediafile okay.. ", end = "")


def getimg(mediafile):

    """ Acquires numpy array from media file, video or image """

    try:
        cap = cv2.VideoCapture(mediafile)
        _, img = cap.read()
    except:
        img = cv2.imread(mediafile)

    return img


def get_vid_params(vid):

    fps = int(vid.get(cv2.CAP_PROP_FPS))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fcount = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    return fps, width, height, fcount


def videowriter(filein, w, h, fps, resizeval):

    ''' Creates a vidout instance using the opencv VideoWriter class '''

    #fourcc = cv2.VideoWriter_fourcc("M","P","4","V")
    fileout = filein[:-5] + ".mp4"
    viddims = (w, h) if resizeval == 1 else (int(w*resizeval), int(h*resizeval))
    vidout = cv2.VideoWriter(fileout, 0x00000020, fps, viddims)

    return vidout


def safe_count(vidfile):

    """ Returns a safe total framecount of a video by going
        through the video frame-by-frame
    """

    cap = cv2.VideoCapture(vidfile)
    vidlength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1

    print("video had", vidlength-count, "non-existing frames.. ", end = "")

    return count


def crop(image, pt1, pt2):

    """ Returns an imaged cropped to a region of interest
        based on topleft and bottomright corner
    """

    cropped = image[pt1[1]:pt2[1], pt1[0]:pt2[0]]

    return cropped


def newdims(img = None, resize = 1, dims = None):

    """ Returns new dimensions based on resize value"""

    if dims is None:
        if img is not None:
            dims = (img.shape[1],img.shape[0])
        else:
            print("No img or dims provided..")
            return

    width = int(dims[0] * resize)
    height = int(dims[1] * resize)

    return (width, height)


def imresize(img, resize = 1, dims = None, back = False):

    """
    Returns resized image based on resizevalue or provided dims

    Parameters
    ----------
    img : numpy array
    resize : float, default = 1
        Multiplier for image size
    dims : tuple, default = None
        Dimensions of the to-be returned image
    back : bool, default = False
        If the inverse of the resize value should be used
    """

    if dims is None:
        resize = 1/resize if back else resize
        dims = newdims(img, resize)

    interpol = cv2.INTER_CUBIC if resize > 1 else cv2.INTER_AREA
    img = cv2.resize(img, dims, interpolation = interpol)

    return img


def add_transimg(bgimg, transimg, offsets):

    """
    Adds a semi-transparent (4-channel) image to a 3-channel background
    image. Images are arrays.
    """

    h, w, c = transimg.shape
    fix = np.zeros((h, w, 3), np.uint8)
    a = transimg[:, :, 3] / 255.0  #alpha
    o = offsets
    fix[:,:,0] = (1.-a)*bgimg[o[1]:o[1]+h, o[0]:o[0]+w, 0]+a*transimg[:,:,0]
    fix[:,:,1] = (1.-a)*bgimg[o[1]:o[1]+h, o[0]:o[0]+w, 1]+a*transimg[:,:,1]
    fix[:,:,2] = (1.-a)*bgimg[o[1]:o[1]+h, o[0]:o[0]+w, 2]+a*transimg[:,:,2]
    bgimg[o[1]:o[1]+h, o[0]:o[0]+w] = fix

    return bgimg


def textdims(text, fontsize, thickness = 1):

    tw, th = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontsize, thickness)[0]

    topy = fontsize*1 if any(x in ["i","j"] for x in text) else 0
    boty = fontsize*2 if any(x in "Q" for x in text) else 0
    boty = fontsize*7 if any(x in ["g","j","y","p","q"] for x in text) else boty

    return (tw, th), topy, boty


def draw_text(img, text, loc = (0, 0), fontsize = 1, col = (0,0,0), margin = 5,
              thickness = 1, bgcol = None):

    (tw, th), topy, boty = textdims(text, fontsize)

    if bgcol is not None:
        topleftout = (loc[0], loc[1])
        botrightx = loc[0] + margin + tw + margin
        botrighty = loc[1] + margin + th + topy + boty + margin
        botright = (botrightx, botrighty)
        cv2.rectangle(img, topleftout, botrightout, bgcol, -1)

    botlefin = (int(loc[0]+margin), int(loc[1]+margin+th+topy))
    cv2.putText(img, text, botlefin, cv2.FONT_HERSHEY_SIMPLEX, fontsize,
                col, thickness, cv2.LINE_AA)


def draw_crosshair(img, pt):

    cv2.line(img, (pt[0] - 5, pt[1]), (pt[0] + 5, pt[1]), namedcols("white"), 1)
    cv2.line(img, (pt[0], pt[1] - 5), (pt[0], pt[1] + 5), namedcols("white"), 1)
