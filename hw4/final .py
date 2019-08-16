from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime
import numpy as np
import imutils
import math


def direction_text(image,deg):
	
	if  -135< deg < -45:
		put_text(image,deg,"Up(North)")
	elif -180< deg< -125:
		put_text(image,deg,"Left(North West)")
	elif 145< deg< 180:
		put_text(image,deg,"Left(West)")
	elif 125 < deg <145:
		put_text(image,deg,"Left(South West)")
	elif 45 <deg< 145:
		put_text(image,deg,"Down(South)")
	elif 5< deg < 45:
		put_text(image,deg,"Right(South East)")
	elif 5 < deg <-5:
		put_text(image,deg,"Right(East)")
	else:
		put_text(image,deg,"Right(North East)")
	return image

def put_text(image,deg,direc):
	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	clr = (0, 0, 255)
	cv2.putText(image, " Direction = %s and Slope = %f"%(direc,deg), (20, 30), font, 1, (clr), 2)
	return image

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
rawCapture = PiRGBArray(camera,size=(640,480))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("video_out.avi",fourcc,4,(640,480))
start_time = time.time()
num_arr = []
file = open("hw4_data.txt","w+")
time_thresh = 100
for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=False):
	start_time_ = datetime.datetime.now()
	image = frame.array
	#lower_green= np.array ([40,200,220])
	lower_green = np.array([40,90,100])
	upper_green = np.array([100,255,190])
	#Color Conversion and Mask conversion
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	mask= cv2.inRange(hsv,lower_green,upper_green)
	blur = cv2.GaussianBlur(mask,(9,9),0)
	result=cv2.bitwise_and(hsv, hsv, mask=mask)
	corners = cv2.goodFeaturesToTrack(blur,5,0.03,20)
	print(corners)
	corners = np.int32(corners)
	# newly added corners codes 
	for i in corners:
		x,y = i.ravel()
		cv2.circle(image,(x,y),4,(0,0,255),-1)

	points=np.array(corners).reshape(5,2)
	num_arr=(0,1,2,3,4)
	rest=[]

	for b in num_arr:
		for c in range(b+1,len(num_arr)):
		 dist = np.linalg.norm(points[b]-points[c])
		 rest.append([dist,b,c])
	rest.sort()
	rest.reverse()
	temp = []
	temp.append(rest[0][1])
	temp.append(rest[0][2])
	temp.append(rest[1][1])
	temp.append(rest[1][2])

	head=-1
	for i in temp:
		if temp.count(i)>1:
		 head=i
		 break
	temp.remove(head)
	temp.remove(head)


	midpoint = (points[temp[0]] + points[temp[1]])/2

	dir = points[head] - midpoint

	myradians = math.atan2(dir[1], dir[0])
	mydegrees = math.degrees(myradians)
	#print(mydegrees)

	cv2.circle(image,(int(midpoint[0]),int(midpoint[1])),4,(0,0,255),-1)
	image = direction_text(image,mydegrees)
#old code
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
