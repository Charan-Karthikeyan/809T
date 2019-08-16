import RPi.GPIO as gpio
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import numpy as np
import cv2

trig = 16
echo  = 18

def distance():
	gpio.setmode(gpio.BOARD)
	gpio.setup(trig,gpio.OUT)
	gpio.setup(echo,gpio.IN)

	gpio.output(trig,False)
	time.sleep(0.01)

	#Generate trigger pulse
	gpio.output(trig,True)
	time.sleep(0.00001)
	gpio.output(trig,False)

	#Generate Echo Time signal 
	while gpio.input(echo)==0:
		pulse_start = time.time()
	while gpio.input(echo) == 1:
		pulse_stop = time.time()

	pulse_duration = pulse_stop - pulse_start

	#Convert the time duration into distance 
	distance  = round(pulse_duration*17150,2)

	#Cleanup 
	gpio.cleanup()
	print("The Distance is",distance," cm")
	return distance 


time_arr = []

for i in range(10):
	time_arr.append(distance())

final_value  = np.mean(time_arr)

camera = PiCamera()
rawCapture = PiRGBArray(camera)

camera.capture(rawCapture,format = 'bgr')
image = rawCapture.array

#cv2.putText(image, "Average Distance = %f cm"%(final_value), (20, 30),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, ((0,0,255)), 2)
#cv2.imshow("image",image)
cv2.imwrite("temp.jpg",image)
cv2.waitKey(0)
cv2.destroyAllWindows()