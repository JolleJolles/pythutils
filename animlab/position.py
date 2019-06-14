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

def positioncam(res = (832,624), compensation = 0):

    """
    Videostream of raspberry pi with cross to accurately position the camera
    """

    cam = PiCamera()
    cam.resolution = res
    cam.framerate = 32
    cam.zoom = (0.0,0.0,1.0,1.0)
    cam.exposure_compensation = compensation

    rawCapture = PiRGBArray(cam)

    time.sleep(0.1)

    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array

        cv2.line(image, (1,1), (res[0], res[1]), color=(255,255,255), thickness=2)
        cv2.line(image, (res[0], 1), (1, res[1]), color=(255,255,255), thickness=2)
        cv2.imshow("Image", image)
        k = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if k == 27:
            break

    cam.close()
    cv2.destroyWindow('Image')
    cv2.waitKey(1)
