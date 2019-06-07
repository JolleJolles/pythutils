# AnimLab
**Python toolset for the mechanistic study of animal behaviour**

![logo](https://github.com/JolleJolles/animlab/blob/master/animlab-logo.jpg)

AnimLab is a collection of methods for Python to facilitate the automated recording, tracking, and processing of data with the Behavioural Scientist in mind. All code is written and documented in such a way that its functionality should be easy to use for people with very limited coding experience.

Installation
------------

To install animlab, simply open a terminal window and enter:
```bash
pip install git+https://github.com/JolleJolles/animlab.git
```

Dependencies
------------

- [Python 2.7 or 3.x](http://www.python.org)

- [numpy](http://www.numpy.org)

- [pandas](https://pandas.pydata.org)

- [pyyaml](https://pyyaml.org)

- [matplotlib](http://matplotlib.org)

- [OpenCV](http://opencv.org)<sup>1</sup>

- [ffmpeg](http://ffmpeg.org)<sup>2</sup>

<sup>1</sup> OpenCV is required only for some of the functionality of AnimLab. For installing python with OpenCV on either Mac, Ubunto, or Raspberry Pi, follow the tutorial in the documentation [here](https://github.com/JolleJolles/animlab/tree/master/docs/install-opencv.md).

<sup>2</sup> FFmpeg is required only for the convert functionality of Animlab. For installing ffmpeg on Mac OS follow the tutorial [here](https://github.com/JolleJolles/animlab/blob/master/docs/install-ffmpeg-for-mac.md) and for the RaspberryPi [here](https://github.com/JolleJolles/animlab/blob/master/docs/install-ffmpeg-with-h264.md).

Example
--------
To use utility functions, e.g.:

    >>> from animlab.utils import listfiles
    >>> from animlab.imutils import crop
    >>> from animlab.mathutils import points_to_angle
    >>> from animlab import Converter

Development
--------
For an overview of version changes see the [CHANGELOG](https://github.com/JolleJolles/animlab/blob/master/CHANGELOG) and for detailed changes see the [commits page](https://github.com/JolleJolles/animlab/commits/). Please submit bugs or feature requests to the GitHub issue tracker [here](https://github.com/JolleJolles/animlab/issues).

License
--------
Released under a Apache 2.0 License. See [LICENSE](https://github.com/JolleJolles/animlab/blob/master/LICENSE) for details.
