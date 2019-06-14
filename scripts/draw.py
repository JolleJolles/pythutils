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

# A simple script that draws a crosshair and rectangle Dynamically

import cv2
import numpy as np
import animlab.imutils as alimu

mouse = animu.mouse_events()

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse.draw)

while(1):
    frame = np.zeros((512,512,3), np.uint8)+55
    draw_frame = frame.copy()

    alimu.draw_crosshair(draw_frame, mouse.pointer)
    alimu.draw_rectangle(draw_frame, mouse.pointer, mouse.rect, mouse.drawing)

    cv2.imshow('image', draw_frame)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
