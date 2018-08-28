# AnimLab
**Sophisticated computational tools for studying animal behaviour**


Installation
------------

Install or upgrade to the latest version:
```bash
pip install git+https://github.com/joljols/animlab.git
```
```bash
pip2 install --upgrade git+https://github.com/joljols/animlab.git
```

Dependencies
------------

- [Python 2.7+](http://www.python.org)

- [numpy](http://www.numpy.org/)

- [pandas](https://pandas.pydata.org)

- [pyyaml](https://pyyaml.org)

- [matplotlib](http://matplotlib.org/)

- [OpenCV](http://opencv.org/)

**Note**: Not all dependencies are installed automatically as some packages (like
Matplotlib) take considerable time, especially on the RPi, and may only be
required in specific cases. Please install these manually when required using
`pip`.


Example
--------
To use utility functions, e.g.:

    >>> from animlab.utils import listfiles
    >>> from animlab.imutils import crop
    >>> from animlab.mathutils import points_to_angle
