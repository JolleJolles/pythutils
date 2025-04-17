#!/usr/bin/env python
# Copyright (c) 2018 - 2025 Jolle Jolles <j.w.jolles@gmail.com>
# Licensed under the Apache License, Version 2.0

from __future__ import division
from __future__ import print_function

import os
import cv2
import numpy as np

from pythutils.fileutils import get_ext
from pythutils.mathutils import closenr, sort_points


def check_media(source, internal=False):

    """Runs some basic checks on a mediafile or stream"""

    ext = get_ext(str(source))
    ftype = None
    if ext in [".mov",".mp4",".avi"]:
        ftype = "vid"
    if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
        ftype = "img"
    if type(source) == int:
        ftype = "stream"
    if ftype == None:
        print("File neither video or image file..")
        return False

    if ftype == "img" or ftype == "vid":
        filedir = os.path.dirname(source)
        if filedir != "":
            if not os.path.isdir(filedir):
                print("File directory does not exist..")
                return False
        if not os.path.isfile(source):
            print("File does not exist..")
            return False

    if ftype == "vid" or ftype == "stream":
        cap = cv2.VideoCapture(source)
        flag, frame = cap.read()
        if not flag:
            print("Video source opened but failed to read images..")
            return False

    if not internal:
        print("Mediafile okay.. ", end = "")

    return True


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
        if get_ext(mediafile) not in [".mov",".mp4",".avi"]:
            raise TypeError("File not a video..")
        mediafile = cv2.VideoCapture(mediafile)

    if not mediafile.read()[0]:
        raise RuntimeError("Video could not be read..")
    fps = int(mediafile.get(cv2.CAP_PROP_FPS))
    width = int(mediafile.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(mediafile.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fcount = int(mediafile.get(cv2.CAP_PROP_FRAME_COUNT))

    return fps, width, height, fcount


def videowriter(filein, w, h, fps, resizeval = 1):
    """Creates a cv2.VideoWriter object and checks if it opened successfully"""
    from pythutils.fileutils import get_ext

    ext = get_ext(filein)
    fileout = filein[:-len(ext)]+".mp4" if ext!="" else filein+".mp4"

    viddims = (w, h) if resizeval == 1 else (int(w*resizeval), int(h*resizeval))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vidout = cv2.VideoWriter(fileout, fourcc, fps, viddims)

    if not vidout.isOpened():
        print(f"[ERROR] Failed to open VideoWriter for {fileout}")
        return None

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


def crop(image, pt1, pt2=None):

    """Crops image based on based on top left and bottom right corner"""

    if pt2 == None:
        pt2 = pt1[1]
        pt1 = pt1[0]
    cropped = image[pt1[1]:pt2[1], pt1[0]:pt2[0]]

    return cropped


def fourpt_transform(image, pts):

    """
    Perspective transform a section of an image based on four coordinates
    to obtain a top-down view
    """

    rect = sort_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0], [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


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


def picamconv(resolution, maxres = (1632, 1232)):

    """Adapts video resolution to work with raspberry pi camera"""

    width = min(closenr(resolution[0],32), maxres[0])
    height = min(closenr(resolution[1],16), maxres[1])

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
