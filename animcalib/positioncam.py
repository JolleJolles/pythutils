# coding: utf-8

# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Initialize the camera
camera = PiCamera()
camera.resolution = (832, 624)
camera.framerate = 32
camera.zoom = (0.0,0.0,1.0,1.0)
camera.exposure_compensation = 0

# Grab a reference to the raw camera capture
rawCapture = PiRGBArray(camera)

# Allow the camera to warmup
time.sleep(0.1)

# Show camera stream
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array

    # Draw diagonal lines from the corners
    cv2.line(image, (1,1), (832, 624), color=(255,255,255), thickness=2)
    cv2.line(image, (832, 1), (1, 624), color=(255,255,255), thickness=2)

    cv2.imshow("Image", image)
    k = cv2.waitKey(1) & 0xFF

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    if k == 27:
        break
