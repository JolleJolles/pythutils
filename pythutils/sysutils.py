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

class Logger(object):

    """
    Class to log the output of the command line to a log file. Should be written
    to sys.stdout, e.g. sys.stdout = Logger("log.txt"). Output is written to
    file after python instance is closed.
    """

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


def removeline(linenr=1):

    """Removes printed lines in terminal. Linenr starts with current line"""

    for _ in range(linenr):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


def lineprint(text, stamp=True, sameline=False, newline=True, reset=False,
              **kwargs):

    """
    Advanced printing functionality. Can add a simple timestap at the start of
    the to be printed line with the hostname (stamp=True) or with a custom label
    (stamp=True, label=CUS), add text add the end of the previous line of text
    (sameline=True), or overwrite the previous line completely (sameline=True,
    reset=True). To not have whiteline at beginning of new lineprint add
    newline=False.
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
        text = time.strftime("%H:%M:%S") + " [" + label + "] - " + text

    if sameline:
        if reset:
            line = text
            sys.stdout.write("\r")
            sys.stdout.write(" "*100)
        else:
            text = line + " " + text
        line = "\r" + text
        print(line, end="\r")
    elif newline:
        line = "\n"+text
        print(line, end="\r")
    else:
        line = text
        if line == "":
            print(line, end=' ')
        else:
            print(text, end="\r")


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
                    if value not in ('BCM2708','BCM2709','BCM2835','BCM2836'):
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
