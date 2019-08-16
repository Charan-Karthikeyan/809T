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

trig = 16
echo = 18
sum=0
average=0
camera_stat = False


def distance():
	#init()
	#gpio.cleanup()
	#gpio.setwarnings(False)
	avg_dist = []
	print("Getting the distance")
	for i in range(10):
		gpio.setmode(gpio.BOARD)
		gpio.setup(trig, gpio.OUT)
		gpio.setup(echo, gpio.IN)

		gpio.output(trig, False)
		time.sleep(0.01)
		
		#generate trigger pulse
		gpio.output(trig, True)
		time.sleep(0.00001)
		gpio.output(trig,False)
		print("Reading the Distance",gpio.input(echo))
		while gpio.input(echo) == 0:
			pulse_start = time.time()
			#print("Pulse start is ",pulse_start)

		while gpio.input(echo) == 1:
			pulse_end = time.time()
		print("Out of loop ")
		pulse_duration = pulse_end - pulse_start

		# convert time to distacne 
		distance = pulse_duration*17150
		distance = round(distance, 2)
		avg_dist.append(distance)

	#cleanup gpio pims and return the disatmce 	
	avg_dist = np.mean(avg_dist)
	print("got the distance",distance)
	gpio.cleanup()
	return avg_dist

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(31,gpio.OUT)
	gpio.setup(33,gpio.OUT)
	gpio.setup(35,gpio.OUT)
	gpio.setup(37,gpio.OUT)

	gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)
	gpio.setup(7,gpio.IN,pull_up_down = gpio.PUD_UP)


def gameover():
	gpio.output(31,False)
	gpio.output(33,False)
	gpio.output(35,False)
	gpio.output(37,False)
	gpio.cleanup()

def revs_ticks(final_dist):

	revs = (120/(2*math.pi* 0.0325)) * final_dist
	## for Ticks
	ticks = (960/(2*math.pi* 0.0325)) * final_dist
	return revs, ticks


def turn(deg):
	circu = 2*math.pi*0.1007
	arc_lenght = (deg/360)*circu
	## revs calculation
	revs = (120/(2*math.pi* 0.0325)) * arc_lenght
	## Ticks Calculation
	ticks = (960/(2*math.pi* 0.0325)) * arc_lenght
	return revs, ticks

def execute(distance,pwm1,pwm2,val,final_ticks,event):
	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0) 
	dist = 0
	final_dist = distance
	if event == "a":
		# Final Values to the PWM for forward
		pwm1.start(val-4)
		pwm2.start(val+1)	
	elif event == 's':
		pwm1.start(val-1)
		#pwm2.start(val+62)
		pwm2.start(val+62)
	
	else:
		pwm1.start(val)
		pwm2.start(val)
	time.sleep(0.1)
	for i in range(0,1000000000):
		#print()
		if int(gpio.input(12)) != int(buttonBR):
			buttonBR = int(gpio.input(12))
			counterBR += 1

		if int(gpio.input(7)) != int(buttonFL):
			buttonFL = int(gpio.input(7))
			counterFL += 1

		if counterFL < counterBR and event != 's':
			#print("duty cycle change",counterFL,counterBR)
			pwm2.ChangeDutyCycle(val+5)
			
		if counterFL > counterBR and event != 's':
			#print("changing duty cycle",counterFL,counterBR)
			pwm1.ChangeDutyCycle(val+5)

		if counterFL < counterBR and event == 's':
			#print("for reverse front left",counterFL,counterBR)
			pwm2.ChangeDutyCycle(val+7)
			
		if counterFL > counterBR and event == 's':
			#print("for reverse",counterFL,counterBR)
			pwm1.ChangeDutyCycle(val+5)
		
		#print(final_ticks)
		if counterBR >= final_ticks and counterFL >= final_ticks and (event == 'w' or event == 's') :
			print("Travelled",final_dist,"meters")
			break
		elif (counterFL >= final_ticks  and counterBR >= final_ticks) and event =='a':
			print('Travelled for ',final_dist,"angle")
			break
		elif counterFL >= final_ticks and counterBR >= final_ticks *1.4 and event == 'd':
			print('Travelled in  ',final_dist,"angle")
			break
	gpio.cleanup()
	
def forward(inp):
	init()
	pwm1 = gpio.PWM(31,50)
	pwm2= gpio.PWM(37,50)
	val = 30
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'w')
	#print("Moved Forward")


def reverse(inp):
	pwm1 = gpio.PWM(33,50)
	pwm2= gpio.PWM(35,50)
	val = 30
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'s')
	#print("Moved Backward")


def right(inp):
	pwm1 = gpio.PWM(31,50)
	pwm2= gpio.PWM(35,50)
	val = 80
	#distance = inp
	final_dist,final_ticks = turn(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'d')
	#print("Pivoted Right")


def left(inp):
	pwm1 = gpio.PWM(33,50)
	pwm2= gpio.PWM(37,50)
	val = 70
	#distance = inp
	final_dist,final_ticks = turn(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'a')
	#print("Pivoted Left")

def pos(l,theta):
	new_x= l*(math.cos(theta*(3.14/180)))
	new_y= l*(math.sin(theta*(3.14/180)))
	return new_x,new_y,theta

def closeg():
	
	gpio.setmode(gpio.BOARD)
	gpio.setup(36, gpio.OUT)
	pwm = gpio.PWM(36, 50)
	pwm.start(5)
	pwm.ChangeDutyCycle(3.5)
	time.sleep(2)

def openg():
	gpio.setmode(gpio.BOARD)
	gpio.setup(36, gpio.OUT)
	pwm = gpio.PWM(36, 50)
	pwm.start(5)
	pwm.ChangeDutyCycle(9.5)
	time.sleep(2)	

def em():
	cmd = 'python3 email01.py'
	os.system(cmd)

def main():
	init()
	camera = PiCamera()
	camera.rotation = 180
	rawCapture = PiRGBArray(camera, size=(640,480))
	camera.resolution = (640,480)
	camera.start_preview() 
	time.sleep(2)
	camera.capture('hsvcalib.jpg')
	camera.stop_preview()
	image =cv2.imread("hsvcalib.jpg")
	lower_red= np.array ([0,150,82])

	upper_red = np.array([5,231,222])

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask= cv2.inRange(hsv,lower_red,upper_red)
	result=cv2.bitwise_and(hsv, hsv, mask=mask)
	blur = cv2.GaussianBlur(mask,(9,9),0)
	#cv2.imwrite('hsv.jpg',hsv)
	#cv2.imwrite('result.jpg',result)
	cv2.drawMarker(image,(320,240),1 )
	ret,thresh = cv2.threshold(blur,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(image, contours, -1, (0,0,255), 3)
	# Find the index of the largest contour
	areas = [cv2.contourArea(c) for c in contours]
	if areas !=[]:
		print(areas)
		max_index = np.argmax(areas)
		camera_stat = True
		cnt=contours[max_index]
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius=int(radius)
		cv2.circle(image,center,radius,(0,255,0),2)
		cv2.circle(image,center,1,(0,255,255),2)
#cv2.imshow('o',image)
	#cv2.waitKey(0)
		degblock=0
		time.sleep
		if x>340:
			degblock= (x-640/2)*0.061
			right(degblock)
		if x<290:
			degblock=abs((x-(640/2))*0.061)
			left(degblock)
		time.sleep(2)
		camera.close()
		print("The value of x is",x)
		gpio.cleanup()
		if x>280 and x<350:
			print("In the loop")
			dist=distance()
			
			if 24<dist<100:
				forward(0.1)
			if 2< dist<24:
				print("opening gripper")
				openg()
				time.sleep(2)
				forward(0.05)
				closeg()
				photo = input("Do you want to take photo")
				if photo == 'y':
					em()
					camera_stat = False
			if dist>100:
				closeg()
	else:
		camera_stat = False
	print("The camera stat")
	return camera_stat
		# gpio.cleanup()

for i in range(0,1000):
	stat = main()
	if stat != True:
		print("Exitting")
		break
	print(i)

gameover()


	



	



	