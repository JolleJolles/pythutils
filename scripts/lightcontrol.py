#!/usr/bin/python

#Python 2 and 3 compatibility
from __future__ import print_function
from builtins import input

#Load libraries
import RPi.GPIO as GPIO
import sys
import pickle

#Turn off GPIO warnings
GPIO.setwarnings(False)

#Set the GPIO numbering convention to header pin numbers
GPIO.setmode(GPIO.BOARD)

#Show state on same line
def showstate(end=". "):
	global state
	state = "on" if GPIO.input(pin) == 1 else "off"
	sys.stdout.write('\x1b[1A')
	sys.stdout.write('\x1b[2K')
	print(light,"is now",state,end=end)

#Set up the pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

#Set the light
lighttype = input("Set normal (n) or IR (i) led strip: ")
if lighttype == "n":
	light = "normal LED"
	pin = 16
if lighttype == "i":
	light = "IR LED"
	pin = 12
showstate()

#Change state
othstate,statement = [0,"off"] if state == "on" else [1,"on"]
change = input("Turn light "+statement+"? ")
if change == "y":
	GPIO.output(pin, othstate)
showstate(end="\n")

#Write state to bootfile
with open("/home/pi/boot/ledstates", "w") as f:
	pickle.dump([GPIO.input(16),GPIO.input(12)], f)
