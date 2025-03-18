#! /usr/bin/env python
# Copyright (c) 2018 - 2019 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import io
import os
import re
import sys
import time
import socket
import fractions
from objsize import get_deep_size

class Suppressor(object):

    """Suppressed the output of a function"""
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, type, value, traceback):
        sys.stdout = self.stdout
        if type is not None:
            print("exception")

    def write(self, x): pass


class Logger(object):

    """
    Class to log output of the command line to a log file
    """

    def __init__(self, filename):
        self.filename = filename

    class Transcript:
        def __init__(self, filename):
            self.terminal = sys.stdout
            self.log = open(filename, "a")
        def __getattr__(self, attr):
            return getattr(self.terminal, attr)
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
        def flush(self):
            pass

    def start(self):
        sys.stdout = self.Transcript(self.filename)

    def stop(self):
        sys.stdout.log.close()
        sys.stdout = sys.stdout.terminal


class objectview:

    """Transforms dictionary into an object"""

    def __init__(self, dic):
        self.__dict__ = dic


def get_size(object):

    """Gets the size in bytes of an object"""

    size_bytes = get_deep_size(object)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return "%s %s" % (s, size_name[i])


def removeline(linenr=1):

    """Removes printed lines in terminal. Linenr starts with current line"""

    for _ in range(linenr):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


def lineprint(text, stamp=True, newline=True, date=False, **kwargs):

    """
    Print text with simple timestap (stamp=True) and hostname (label=XXX) added
    """

    global line, label

    def _vardefined(var):

        return var in [var for var,_ in globals().items()]

    line = line if _vardefined("line") else ""
    label = label if _vardefined("label") else socket.gethostname()
    if not _vardefined("label"):
        label = ""

    if "label" in kwargs:
        label = kwargs["label"]

    if stamp:
        datecode = "%y/%m/%d - %H:%M:%S" if date else "%H:%M:%S"
        text = time.strftime(datecode) + " [" + label + "] - " + text

    if newline:
        print(text)
    else:
        print(text, end=" ")


def homedir():

    """Returns the home directory"""

    return os.path.expanduser("~")+"/"


def isscript():

    """Determines if session is script or interactive (jupyter)"""

    import __main__ as main
    return hasattr(main, '__file__')


def isrpi(message=False):

    """Checks if current system is a Raspberry Pi"""

    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    label, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value not in ('BCM2708','BCM2709','BCM2835','BCM2836',
                                     'BCM2837','BCM2837B0','BCM2711'):
                        return False
            if not found:
                raise ValueError("""Unable to determine if system is rpi or
                                 not. Set system manually""")

    except IOError:
        if message:
            lineprint("non-rpi system detected..")
        return False

    if message:
        lineprint("rpi system detected..")
    return True


def checkfrac(input):

    """Checks string for Fractions and converts them accordingly"""

    transformed_text = re.sub(r'([\d.]+)', r'fractions.Fraction("\1")', input)

    return eval(transformed_text)

def get_google_drive_path():
    """Automatically detect Google Drive location on macOS and Windows."""
    
    # Check common macOS paths
    macos_paths = [
        os.path.expanduser("~/Google Drive"),  # Older Google Drive location
        os.path.expanduser("~/Library/CloudStorage/GoogleDrive-*"),  # Newer macOS location
        "/Volumes/GoogleDrive-*",  # Mounted volume location
    ]

    for path in macos_paths:
        # Use glob to match wildcard paths (GoogleDrive-XXXXX)
        matched_paths = glob.glob(path)
        if matched_paths:
            return matched_paths[0]  # Return the first match found
    
    # Check common Windows paths
    windows_paths = [
        "G:/My Drive",  # Standard Google Drive path on Windows
        "H:/My Drive",  # Alternative drive letter
    ]

    for path in windows_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("Google Drive path not found. Please set it manually.")
