# Simple script that draws a crosshair and rectangle Dynamically

import cv2
import numpy as np
import animlab.imutils as animu

mouse = animu.mouse_events()

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse.draw)

while(1):
    frame = np.zeros((512,512,3), np.uint8)+55
    draw_frame = frame.copy()

    animu.draw_crosshair(draw_frame, mouse)
    animu.draw_rectangle(draw_frame, mouse)

    cv2.imshow('image', draw_frame)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
