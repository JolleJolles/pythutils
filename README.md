# AnimLab
**Python toolset for the mechanistic study of animal behaviour**

![logo](https://github.com/JolleJolles/animlab/blob/master/animlab-logo.jpg)

AnimLab is a collection of methods for Python to facilitate the automated recording, tracking, and processing of data with the Behavioural Scientist in mind. All code is written and documented in such a way that its functionality should be easy to use for people with very limited coding experience.

Installation
------------

To install animlab, open a terminal window and enter:
```bash
pip install git+https://github.com/JolleJolles/animlab.git
```

Dependencies
------------

- [Python 2.7 or 3.x](http://www.python.org)

- [numpy](http://www.numpy.org)

- [pandas](https://pandas.pydata.org)<sup>1</sup>

- [pyyaml](https://pyyaml.org)

- [OpenCV](http://opencv.org)<sup>2</sup>

- [ffmpeg](http://ffmpeg.org)<sup>3</sup>

<sup>1</sup> Pandas can be slow to install with pip on a raspberry pi. A much faster way is to install it manually with apt-get: `sudo apt-get install python-pandas`.

<sup>2</sup> OpenCV is required only for some of the functionality of AnimLab. For installing python with OpenCV on either Mac, Ubunto, or Raspberry Pi, follow the tutorial in the documentation [here](https://github.com/JolleJolles/animlab/tree/master/docs/install-opencv.md).

<sup>3</sup> FFmpeg is required only for the convert functionality of Animlab. For installing ffmpeg on Mac OS follow the tutorial [here](https://github.com/JolleJolles/animlab/blob/master/docs/install-ffmpeg-for-mac.md) and for the RaspberryPi [here](https://github.com/JolleJolles/animlab/blob/master/docs/install-ffmpeg-with-h264.md).

Usage
--------
To use utility functions, e.g.:

    from animlab.utils import listfiles
    from animlab.imutils import crop
    from animlab.mathutils import points_to_angle

   
#### Converting video recordings
1. It is very tricky to record to compressed formats like `.mp4` directly with the rpi and therefore videos are standard stored in the `.h264` format. These videos are very hard to open (I only know of VLC player to make it work partly) but luckily we can easily convert them with the `Converter` class of the package.

2. First import the Convert class and read the documentation:

    ```
    from animlab import Converter
    print(Converter.__doc__)
    ```

3. To start recording you can set the `dir` parameter to the directory of videos you would like to convert. If nothing is provided it will attempt to convert videos from the location at which you initiated python.

	```
	dir = "~/Desktop/videos"
	Converter(dir, withframe = True)
	```

4. The `Converter` class makes it possible to simply convert a folder of videos directly or to also add a running framenumber in the top left corner, such as to facilitate the behavioural observations of video recordings. While the former uses `ffmpeg` and is considerably faster, the latter uses `opencv`, with both making use of multiprocessing such that multiple videos can be converted simultaneously. Converting without frame is default (`withframe = False`). To convert videos with the frame number displayed enter:

	`Converter(dir, withframe = True)`

5. It is also possible to resize videos. Simply add the resize value to `resizeval` with which the video should be resized. For example, to make the video half the dimensions of what it was enter:

	`Converter(dir, resizeval = 0.5)`

Development
--------
For an overview of version changes see the [CHANGELOG](https://github.com/JolleJolles/animlab/blob/master/CHANGELOG) and for detailed changes see the [commits page](https://github.com/JolleJolles/animlab/commits/). Please submit bugs or feature requests to the GitHub issue tracker [here](https://github.com/JolleJolles/animlab/issues).

License
--------
Released under a Apache 2.0 License. See [LICENSE](https://github.com/JolleJolles/animlab/blob/master/LICENSE) for details.
