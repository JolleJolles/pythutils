
# coding: utf-8

# In[ ]:


from datetime import datetime
import os

def now(timeformat = "date"):
    
    """ Returns current date or time """
    
    if timeformat == "date":
        return datetime.now().strftime("%y/%m/%d")
    
    elif timeformat == "time":
        return datetime.now().strftime("%H:%M:%S")
    
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

