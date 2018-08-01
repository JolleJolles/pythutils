
# coding: utf-8

# In[ ]:


import cv2

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


def newdims(img = None, dims = None, resize = 1):
    
    """ Returns new dimensions based on resize value"""
    
    if dims is None:
        if img is not None:
            dims = (img.shape[1],img.shape[0])
        else:
            print "No img or dims provided.."
    
    width = int(dims[0] * resize)
    height = int(dims[1] * resize)
    
    return (width, height)


def imgresize(img, resize = 1, dims = None, back = False):                

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

