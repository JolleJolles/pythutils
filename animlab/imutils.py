
# coding: utf-8

# In[ ]:

import os
import cv2
from animlab.utils import *


def check_media(mediafile):
    
    ext = get_ext(mediafile)
    ftype = "vid" if ext in [".mov",".mp4",".avi"] else "img" if ext in [".jpg", ".png", ".jpeg", ".bmp"] else None
    filedir = os.path.dirname(mediafile)

    assert ftype != None, "File neither Video or image file.."    
    assert os.path.isdir(filedir), "File directory does not exist.."    
    assert os.path.isfile(mediafile), "File does not exist.."

    if ftype == "vid":
        cap = cv2.VideoCapture(mediafile)
        assert cap.read()[0], "Video source opened but failed to read any images.." 
    
    print ftype, "file okay!",


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
            print "No img or dims provided.."
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
        resize = 1./resize if back else resize
        dims = newdims(img, resize)
          
    interpol = cv2.INTER_CUBIC if resize > 1 else cv2.INTER_AREA
    img = cv2.resize(img, dims, interpolation = interpol) 

    return img


def textdims(text, fontsize, thickness = 1):
    
    tw, th = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontsize, thickness)[0]
    
    topy = fontsize*1 if any(x in ["i","j"] for x in text) else 0
    boty = fontsize*2 if any(x in "Q" for x in text) else 0
    boty = fontsize*7 if any(x in ["g","j","y","p","q"] for x in text) else boty
    
    return (tw, th), topy, boty


def draw_text(img, text, loc = (0, 0), fontsize = 1, col = (0,0,0), margin = 5, bgcol = None):
     
    (tw, th), topy, boty = textdims(text, fontsize)
    print (tw, th), topy, boty
    print margin
    
    if bgcol is not None:
        topleftout = (loc[0], loc[1])
        botrightout = (loc[0]+margin+tw+margin, loc[1]+margin+th+topy+boty+margin)
        cv2.rectangle(img, topleftout, botrightout, bgcol, -1)

    botlefin = (loc[0]+margin, loc[1]+margin+th+topy)
    cv2.putText(img, text, botlefin, cv2.FONT_HERSHEY_SIMPLEX, fontsize, col, 1, cv2.LINE_AA)
    

def draw_crosshair(img, x, y):
    cv2.line(img, (x - 5, y), (x + 5, y), namedcols("whi"), 1)
    cv2.line(img, (x, y - 5),( x, y + 5), namedcols("whi"), 1)

