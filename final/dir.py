import RPi.GPIO as gpio
import time
import numpy as np 
from matplotlib import pyplot as plt
import math

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
	return revs,ticks

def turn(deg):
	circu = 2*math.pi*0.1007
	arc_lenght = (deg/360)*circu
	## revs calculation
	revs = (120/(2*math.pi* 0.0325)) * arc_lenght
	## Ticks Calculation
	ticks = (960/(2*math.pi* 0.0325)) * arc_lenght

	return revs, ticks

def key_init(event,inp):
	init()
	tf = inp
	if event.lower() == 'w':
		# print("Forward")
		forward(tf,event)
	elif event.lower() == 's':
		# print("Backward")
		reverse(tf,event)
	elif event.lower() == 'a':
		# print("Left")
		left(tf,event)
	elif event.lower() == 'd':
		# print("Right")
		right(tf,event)
	else:
		print("Wrong Keys press 'w','a','s','d', or 'p' to quit")

def execute(distance,pwm1,pwm2,val,final_ticks,event):
	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0) 
	dist = 0
	final_dist = distance
	if event == "a":
		# Final Values to the PWM for forward
		# pwm1.start(val-4)
		# pwm2.start(val+1)
		pwm1.start(val)
		pwm2.start(val+0.001)	
	elif event == 's':
		# pwm1.start(val-1)
		# pwm2.start(val+2)

		pwm1.start(val)
		pwm2.start(val+15)
	# elif event == 'd':
	# 	pwm1.start(val-5)
	# 	pwm2.start(val)
	# elif event == 'a':
	# 	pwm1.start(val)
	# 	pwm2.start(val+2)
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
			print("duty cycle change",counterFL,counterBR)
			pwm1.ChangeDutyCycle(val+5)
			
		if counterFL > counterBR and event != 's':
			print("changing duty cycle",counterFL,counterBR)
			pwm2.ChangeDutyCycle(val+5)
			# pwm2.ChangeDutyCycle(val-5)

		if counterFL < counterBR and event == 's':
			print("for reverse front left",counterFL,counterBR)
			pwm1.ChangeDutyCycle(val+5)
			
		if counterFL > counterBR and event == 's':
			print("for reverse",counterFL,counterBR)
			pwm2.ChangeDutyCycle(val+12)
		
		#print(final_ticks)
		if counterBR >= final_ticks and counterFL >= final_ticks and (event == 'w' or event == 's') :
			print("Travelled",final_dist,"meters")
			break
		elif (counterFL >= final_ticks  and counterBR >= final_ticks*1.1) and event =='a':
			print('Travelled for ',final_dist,"angle")
			break
		elif counterFL >= final_ticks and counterBR >= final_ticks *1.3 and event == 'd':
			print('Travelled in  ',final_dist,"angle")
			break
	gpio.cleanup()


def forward(inp,event):
	# Left wheels 
	pwm1 = gpio.PWM(31,50)
	# Right Wheels
	pwm2= gpio.PWM(37,50)
	val = 30
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,event)
	print("Moved Forward")

def reverse(inp,event):
	#Left Reverse Wheels
	pwm1 = gpio.PWM(33,50)
	#Right Reverse Wheels
	pwm2= gpio.PWM(35,50)
	val = 30
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,event)
	print("Moved Backward")

def right(inp,event):
	pwm1 = gpio.PWM(31,50)
	pwm2= gpio.PWM(35,50)
	val = 70
	#distance = inp
	final_dist,final_ticks = turn(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,event)
	print("Moved Right")

def left(inp,event):
	pwm1 = gpio.PWM(33,50)
	pwm2= gpio.PWM(37,50)
	val = 70
	#distance = inp
	final_dist,final_ticks = turn(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,event)
	print("Moved Left")

while True: 
	key_input = input("Select the driving Keys :")
	
	if key_input == 'p':
		break
	distance_to_travel = float(input("Input Distance or angle :"))
	key_init(key_input,distance_to_travel)

gameover()


