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
from __future__ import print_function

import os
import cv2
import numpy as np

from pythutils.fileutils import get_ext
from pythutils.mathutils import closenr


def check_media(mediafile):

    """Runs some basic checks on a mediafile"""

    ext = get_ext(mediafile)
    vidtypes = [".mov",".mp4",".avi"]
    imgtypes = [".jpg", ".png", ".jpeg", ".bmp"]
    ftype = "vid" if ext in vidtypes else "img" if ext in imgtypes else None
    filedir = os.path.dirname(mediafile)

    assert ftype != None, "File neither video or image file.."
    if filedir != "":
        assert os.path.isdir(filedir), "File directory does not exist.."
    assert os.path.isfile(mediafile), "File does not exist.."

    if ftype == "vid":
        cap = cv2.VideoCapture(mediafile)
        assert cap.read()[0], "Video source opened but failed to read images.."

    print("Mediafile okay.. ", end = "")


def getimg(mediafile):

    """Acquires a numpy array from a video or image"""

    try:
        cap = cv2.VideoCapture(mediafile)
        _, img = cap.read()
    except:
        img = cv2.imread(mediafile)

    return img


def get_vid_params(mediafile):

    """Gets video parameters from file or video instance"""

    if type(mediafile) is str:
        assert get_ext(mediafile) in [".mov",".mp4",".avi"], "File not a video.."
        mediafile = cv2.VideoCapture(mediafile)

    assert mediafile.read()[0], "Video could not be read.."
    fps = int(mediafile.get(cv2.CAP_PROP_FPS))
    width = int(mediafile.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(mediafile.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fcount = int(mediafile.get(cv2.CAP_PROP_FRAME_COUNT))

    return fps, width, height, fcount


def videowriter(filein, w, h, fps, resizeval):

    """Creates a vidout instance using the opencv VideoWriter class"""

    ext = get_ext(filein)
    fileout = filein[:-len(ext)]+".mp4" if ext!="" else filein+".mp4"
    viddims = (w, h) if resizeval == 1 else (int(w*resizeval), int(h*resizeval))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vidout = cv2.VideoWriter(fileout, fourcc, fps, viddims)

    return vidout


def safe_framecount(vidfile):

    """Saves video frame counter that counts frame-by-frame"""

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

    """Crops image based on based on top left and bottom right corner"""

    cropped = image[pt1[1]:pt2[1], pt1[0]:pt2[0]]

    return cropped


def checkroi(roi, resolution):

    """Make sure roi coordinates are within resolution"""

    x1 = max(roi[0][0],1)
    y1 = max(roi[0][1],1)
    x2 = min(roi[1][0],resolution[0])
    y2 = min(roi[1][1],resolution[1])

    return ((x1,y1),(x2,y2))


def zoom_to_roi(zoom, resolution):

    """Gets region of interest coordinates from x,y,w,h zoom parameters"""

    x1 = int(zoom[0] * resolution[0])
    x2 = int((zoom[0]+zoom[2]) * resolution[0])
    y1 = int(zoom[1] * resolution[1])
    y2 = int((zoom[1]+zoom[3]) * resolution[1])

    return ((x1,y1),(x2,y2))


def roi_to_zoom(roi, resolution):

    """Gets x,y,w,h zoom parameters from region of interest coordinates"""

    ((x1,y1),(x2,y2)) = roi
    z0 = round(x1 / resolution[0],2)
    z1 = round(y1 / resolution[1],2)
    z2 = round((x2-x1) / resolution[0],2)
    z3 = round((y2-y1) / resolution[1],2)

    return (z0, z1, z2, z3)


def picamconv(resolution):

    """Adapts video resolution to work with raspberry pi camera"""

    width = closenr(resolution[0],32)
    height = closenr(resolution[1],16)

    return (width, height)


def fix_vidshape(res1,res2):

    """Compares two resolutions and get missing x and y coords"""

    xmin,ymin = 0,0
    xmult = (res2[0]/res1[0])
    ymult = (res2[1]/res1[1])
    if xmult > ymult:
        xmin = int((res2[0]-(res1[0]*ymult))/2)
    if ymult > xmult:
        ymin = int((res2[0]-(res1[0]*xmult))/2)

    return xmin, ymin


def newdims(img = None, resize = 1, dims = None):

    """Returns new dimensions of an image array based on resize value"""

    if dims is None:
        if img is None:
            print("No img or dims provided..")
            return
        else:
            dims = (img.shape[1],img.shape[0])

    width = int(dims[0] * resize)
    height = int(dims[1] * resize)

    return (width, height)


def imgresize(img, resize = 1, dims = None, back = False):

    """
    Returns resized image based on resizevalue or provided dimensions

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
    image. Images need to be arrays.
    """

    h, w, c = transimg.shape
    fix = np.zeros((h, w, 3), np.uint8)
    a = transimg[:, :, 3] / 255  #alpha
    o = offsets
    fix[:,:,0] = (1.-a)*bgimg[o[1]:o[1]+h, o[0]:o[0]+w, 0]+a*transimg[:,:,0]
    fix[:,:,1] = (1.-a)*bgimg[o[1]:o[1]+h, o[0]:o[0]+w, 1]+a*transimg[:,:,1]
    fix[:,:,2] = (1.-a)*bgimg[o[1]:o[1]+h, o[0]:o[0]+w, 2]+a*transimg[:,:,2]
    bgimg[o[1]:o[1]+h, o[0]:o[0]+w] = fix

    return bgimg
