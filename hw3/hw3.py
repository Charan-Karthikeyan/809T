#!/usr/bin/python
# -*- coding: utf-8 -*-

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime
import numpy as np
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640,480))
fourcc = cv2.VideoWriter_fourcc(*'XVID')	
out = cv2.VideoWriter('videoname1.avi', fourcc, 3, (640, 480))
f=open('hw3data.txt','a')


# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
	start=datetime.datetime.now()
	image=frame.array
	cv2.imshow("Frame", image)
	lower_green= np.array ([70,200,100])
	upper_green = np.array([90,255,190])
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask= cv2.inRange(hsv,lower_green,upper_green)
	_, contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	result=cv2.bitwise_and(hsv, hsv, mask=mask)
	cv2.drawContours(image,contours,-1,(240,250,160),3)
	hor=np.hstack((image,hsv,result))
	cv2.imshow("1st part",hor)
 	
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord("q"):  
	 break
	stop=datetime.datetime.now()
	now=stop-start
	outstring=str(now.total_seconds())+'\n'
	f.write(outstring)
	print(now.total_seconds())
	out.write(image)