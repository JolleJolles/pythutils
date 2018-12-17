# Install guide
AnimLab is a collection of python packages to facilitate the automated recording, tracking, and processing behavioural experimental data. All code is written and documented in such a way that its functionality should be easy to use for scientists with very limited coding experience. This document provides a brief tutorial for how to set up an environment to work with AnimLab's various functionalities.

AnimLab is both python 2.x and python 3.x compatible and makes strong use of the [numpy](http://www.numpy.org/) and [OpenCV](http://opencv.org/) libraries. In addition, much of its functionality is best use in combination with the [jupyter interface](https://jupyter.org). This guide will help you 1. install python with opencv on your system (steps for the different operating systems are provided), 2. install necessary python packages, including the various AnimLab packages, 3. install jupyter.

**Note**: At this moment only the utilities package *animlab* is publicly available as I the *animrec* and *animtrack* packages are still in beta. For installing those, please use the credentials privately send by me.

1. Install python with opencv
------------
Unfortunately installing python with opencv is not as simple as just downloading an installer from the internet and running that. At the same time, it is not super complicated when carefully following the right steps. I have created a special gist with a full overview of the necessary steps for installing python with opencv on mac here: https://git.io/fpyvq. Installing python with opencv on the other operating systems will follow later.

2. Install the necessary packages
------------
Using terminal, make sure you are in the right virtual environment e.g. `workon(py3cv)`. To install packages we will use `pip`, like we did in step 1 above. The most basic requirements in addition to *numpy* and *opencv* are:
`pip install pandas matplotlib pyyaml csv itertools`

Now we can install the animlab utilies package:
`pip install git+https://github.com/JolleJolles/animlab.git`

To install the *animtrack* package we will need install a number of additional packages:
`pip install scipy pickle h5py warnings collections PIL ast math pathos random subprocess`
`pip install git+https://github.com/jolleslab/animtrack.git`

Similarly, to install the *animrec* package we will need install some additional packages. Furthermore, animrec (currently) only works on the Raspbian operating system so make sure this is done on a Raspberry Pi:
`pip install socket picamera localconfig==0.4.2`
`pip install git+https://github.com/jolleslab/animrec.git`

As *animtrack* and *animrec* are still in beta, an alternative way to install the packages is from the zip file of the repository provided. For animrec:
`cd animrec-master`
`pip install -e .`

And for animtrack:
`cd animtrack-master`
`pip install -e .`

3. Installing and working with jupyter
------------
Jupyter is very simple to install with pip again (making sure you are in the right virtual environment):
`pip install jupyter`

Now to run jupyter, simply enter `jupyter notebook` in terminal and press Enter.
