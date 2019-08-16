import cv2 
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np 
camera  = PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
rawCapture = PiRGBArray(camera,size = (640,480))
def capture_frame():
	camera.start_preview()
	camera.capture(rawCapture,format='bgr')
	image = rawCapture.array
	#cv2.imshow('Frame',image)
	image = cv2.flip(image,-1)
	cv2.imshow('Frame',image)
	cv2.imwrite("new.jpg",image)
	cv2.waitKey()
	cv2.destroyAllWindows() 
capture_frame()
#image = cv2.imread("inv_image.jpg")
