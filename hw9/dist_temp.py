import RPi.GPIO as gpio
import time
import numpy as np 
from matplotlib import pyplot as plt
import math
import os
from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray
import cv2
import imutils
import picamera
from time import sleep
from PIL import Image

# trig = 13
# echo = 40
sum=0
average=0


def distance(trig,echo):
	#init()
	#gpio.cleanup()
	#gpio.setwarnings(False)
	#print("Getting the distance")
	gpio.setmode(gpio.BOARD)
	gpio.setup(trig, gpio.OUT)
	gpio.setup(echo, gpio.IN)

	gpio.output(trig, False)
	time.sleep(0.01)
	
	#generate trigger pulse
	gpio.output(trig, True)
	time.sleep(0.00001)
	gpio.output(trig,False)
	##print("Reading the Distance",gpio.input(echo))
	while gpio.input(echo) == 0:
		up = True
		pulse_start = time.time()
		#print("Pulse start is ",pulse_start)

	while gpio.input(echo) == 1:
		down = True
		pulse_end = time.time()
	# print("Out of loop ")
	if up == True and down == True:
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration*17150
		distance = round(distance, 2)

	#cleanup gpio pims and return the disatmce 	
	
		print("got the distance",distance,pulse_duration)
	
	else:
		print("crashed due to problem")
	# convert time to distacne 
	gpio.cleanup()
	return distance

for i in range(2):
	distance(16,18)
	distance(11,38)
	distance(13,40)