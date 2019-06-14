#! /usr/bin/env python
#
# Python toolset for the mechanistic study of animal behaviour
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

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def positioncam(resolution = (832,624), compensation = 0):

    """
    Videostream of raspberry pi with cross to accurately position the camera
    """

    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = 32
    camera.zoom = (0.0,0.0,1.0,1.0)
    camera.exposure_compensation = compensation

    rawCapture = PiRGBArray(camera)

    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array

        cv2.line(image, (1,1), (832, 624), color=(255,255,255), thickness=2)
        cv2.line(image, (832, 1), (1, 624), color=(255,255,255), thickness=2)
        cv2.imshow("Image", image)
        k = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if k == 27:
            break
