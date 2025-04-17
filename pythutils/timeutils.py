#!/usr/bin/env python
# Copyright (c) 2018 - 2025 Jolle Jolles <j.w.jolles@gmail.com>
# Licensed under the Apache License, Version 2.0

from __future__ import print_function

import sys
import time
import datetime

def clock():

    """Simple running clock that prints on the same line"""

    while True:
        print(datetime.datetime.now().strftime("%H:%M:%S"), end="\r")
        sys.stdout.flush()
        time.sleep(1)


def now(timeformat = "date"):

    """Returns current date or time"""

    if timeformat == "date":
        return datetime.datetime.now().strftime("%y/%m/%d")

    elif timeformat == "time":
        return datetime.datetime.now().strftime("%H:%M:%S")

    else:
        print("No right time format provided..")
