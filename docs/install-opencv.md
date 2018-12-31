<small>Copyright (c) 2018 - 2019 Jolle Jolles<br/>
Last updated: 31 Dec 2018</small>

<h2>Install OpenCV for Python on Mac, Ubuntu and Raspberry Pi</h2>
Installing [OpenCV](https://opencv.org) has never been easy and always required a lot of careful usage of the command line to build from source. This was especially painful when working with a Raspberry Pi as building and installing OpenCV took a lot of time on the RPi, especially on the older models. Luckily this has changed very recently as it is now possible to [install OpenCV with pip](https://pypi.org/project/opencv-python)!

Below I guide you through the basic steps that I think are necessary to get opencv to work nicely on Mac, Ubuntu and Raspberry Pi. If you want more background information, see the [excellent article](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) by Adrian Rosebrock from [PyImageSearch.com](http://PyImageSearch.com).

Pip is the main package manager for python that we will also use to install OpenCV. Pip should already be installed on your system (see [here](https://pip.pypa.io/en/stable/installing/)), but if it's not, we can install it with wget. Open a Terminal window and enter:

`wget https://bootstrap.pypa.io/get-pip.py`

Now to install pip for Python 3 enter:

`sudo python3 get-pip.py`

Or if you are still working with Python 2.7, simply enter:

`sudo python get-pip.py`

Next, and for the Raspberry Pi only, we need to install some additional packages. Make sure apt-get is fully up to date by entering the following in Terminal:

`sudo apt-get update`

Now install the prerequisites:

```
sudo apt-get install libhdf5-dev libhdf5-serial-dev
sudo apt-get install libqtwebkit4 libqt4-test
sudo apt-get install libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5
```

Finally, we can enter a wonderfully simple command to install OpenCV:

`sudo pip install opencv-contrib-python`

For those of you also used to installing OpenCV manually I am sure you will be as happy as I am! Now let's just make sure that OpenCV is working. Open a terminal window and enter `python3` to start Python. Now to make sure you have installed OpenCV correctly enter:

```
import cv2
cv2.__version__
```

Your terminal window should look like:

```
$ python3
Python 3.5.3 (default, Sep 27 2018, 17:25:39)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'3.4.4'
```

You are done!
