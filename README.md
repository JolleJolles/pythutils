# AnimLab
**Computational and analytical tools and functions for the mechanistic study of animal behaviour**


Installation
------------

To install, simply open a terminal window and enter:
```bash
pip install git+https://github.com/JolleJolles/animlab.git
```

Dependencies
------------

- [Python 2.7 or 3.x](http://www.python.org)

- [numpy](http://www.numpy.org/)

- [pandas](https://pandas.pydata.org)

- [pyyaml](https://pyyaml.org)

- [matplotlib](http://matplotlib.org/)

- [OpenCV](http://opencv.org/)

For installing python with opencv on mac I have written a concise guide, find it here: https://git.io/fpyvq

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

License
--------
Released under a Apache 2.0 License. See [LICENSE](https://github.com/JolleJolles/animlab/blob/master/LICENSE) for details.
