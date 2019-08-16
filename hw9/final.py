import cv2 
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np 
import io
import RPi.GPIO as gpio
camera  = PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
#rawCapture = PiRGBArray(camera,size = (640,480))
stream  = io.BytesIO()
def capture_frame():
	with picamera.PiCamera as camera():
		camera.start_preview()
		time.sleep(2)
		camera.capture(stream,format = 'jpeg')
	data = np.fromstring(stream.getvalue(),dtype=np.uint8)
	image = cv2.imdecode(data,1)
	return image

def image_process(image):
	image = cv2.flip(image.-1) 
	lower_red = np.array([])
	upper_red = np.array([])
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	mask= cv2.inRange(hsv,lower_green,upper_green)
	blur = cv2.GaussianBlur(mask,(9,9),0)
	result=cv2.bitwise_and(hsv, hsv, mask=mask)
	corners = cv2.goodFeaturesToTrack(blur,5,0.03,20)
	
	corners = np.int32(corners)
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
	
	#cv2.circle(image,midpoint,4,(0,0,255),-1)
	
	return midpoint

def center_axis(image):
	img_shape = image.shape
	#print(img_shape)
	c_x = img_shape[0]/2
	c_y = img_shape[1]/2
	return c_x,c_y

def angle_read():
	




def distance_measure():
	gpio.setmode(gpio.BOARD)
	gpio.setup(trig,gpio.OUT)
	gpio.setup(echo,gpio.IN)

	gpio.output(trig, False)
	time.sleep(0.01)

	gpio.output(trig,True)
	time.sleep(0.0001)
	gpio.output(trig,False)

	while gpio.input(echo) == 0:
		pulse_start = time.time()
	while gpio.input(echo) == 1:
		pulse_end = time.time()

	pulse_duration = pulse_end-pulse_start

	distance = pulse_duration*17150
	distance = round(distance,2)

	gpio.cleanup()
	return distance

def


