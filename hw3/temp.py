from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime
import numpy as np
import imutils

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
rawCapture = PiRGBArray(camera,size=(640,480))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("video_out.avi",fourcc,10,(640,480))
start_time = time.time()
file = open("hw3_data.txt","w+")
time_thresh = 175
for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=False):
	start_time_ = datetime.datetime.now()
	image = frame.array
	lower_green  = np.array([40,200,100])
	upper_green = np.array([90,255,190])
	#Color Conversion and Mask conversion
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	mask= cv2.inRange(hsv,lower_green,upper_green)
	result=cv2.bitwise_and(hsv, hsv, mask=mask)
	#finding the countors in the image
	cnts  = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	if len(cnts) >0:
#		print("the cnts is",cnts)
		c = max(cnts,key = cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		#center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 1:
			cv2.circle(image, (int(x), int(y)), int(radius),(0, 125, 255), 2)
#			print("radius",radius)
		#	cv2.circle(image,center,5,(0,125,255),-1)
	cv2.imshow("frame",image)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key== ord("q"):
		break
	time_out = time.time()-start_time
	if time_out >= time_thresh:
		break

	stop_time = datetime.datetime.now()
	now = stop_time-start_time_
	out_values = str(now.total_seconds())+"\n"
	file.write(out_values)
	print("The time out is",time_out)
	out.write(image)
