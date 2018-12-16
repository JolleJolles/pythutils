#!/usr/bin/python
from __future__ import print_function

import pickle
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

with open("/home/pi/boot/ledstates", "r") as f:
	states = pickle.load(f)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

GPIO.output(16, states[0])
GPIO.output(12, states[1])

print("Normal and IR led strips set to",states)
