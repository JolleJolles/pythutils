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
