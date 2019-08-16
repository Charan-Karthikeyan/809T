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
		forward(tf)
		move.append(inp)
		angle.append(0)
		direc.append('w')
	elif event.lower() == 's':
		# print("Backward")
		reverse(tf)
		move.append(-inp)
		angle.append(0)
		direc.append('s')
	elif event.lower() == 'a':
		# print("Left")
		move.append(0)
		angle.append(inp)
		left(tf)
		direc.append('a')
	elif event.lower() == 'd':
		# print("Right")
		move.append(0)
		angle.append(-inp)
		right(tf)
		direc.append('d')
	else:
		print("Wrong Keys press 'w','a','s','d', or 'p' to quit")

def execute(distance,pwm1,pwm2,val,final_ticks):
	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0)
	dist = 0
	final_dist = distance
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

		if counterFL < counterBR:
			pwm2.ChangeDutyCycle(val+5)

		if counterFL > counterBR:
			pwm1.ChangeDutyCycle(val+5)

		if counterBR >= final_ticks and counterFL >= final_ticks:
			print("Travelled",final_dist,"meters")
			break
	gpio.cleanup()
def pos(l,theta):
	print("the vals are",l, theta)
	vals = theta*(3.14/180)
	new_x= l*(math.cos(vals))
	new_y= l*(math.sin(vals))
	return new_x,new_y,theta


def forward(inp):
	pwm1 = gpio.PWM(31,50)
	pwm2= gpio.PWM(37,50)
	val = 20
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks)
	print("Moved Forward")

def reverse(inp):
	pwm1 = gpio.PWM(33,50)
	pwm2= gpio.PWM(35,50)
	val = 20
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks)
	print("Moved Backward")

def right(inp):
	pwm1 = gpio.PWM(31,50)
	pwm2= gpio.PWM(35,50)
	val = 60
	#distance = inp
	final_dist,final_ticks = turn(inp)
	execute(inp,pwm1,pwm2,val,final_ticks)
	print("Moved Right")

def left(inp):
	pwm1 = gpio.PWM(33,50)
	pwm2= gpio.PWM(37,50)
	val = 70
	#distance = inp
	final_dist,final_ticks = turn(inp)
	execute(inp,pwm1,pwm2,val,final_ticks)
	print("Moved Left")
move=[]
angle=[]
direc = []
coor_x=[0]
coor_y=[0]
counter =0
x=0
y=0
while True: 
	key_input = input("Select the driving Keys :")
	distance_to_travel = float(input("Input Distance or angle :"))
	if key_input == 'p':
		break
	key_init(key_input,distance_to_travel)
	counter+=1
	print(counter)

gpio.cleanup()

for i in range(0,counter):

	angle[i]=angle[i]+angle[i-1]
	print(angle[i],move[i])
	new_x,new_y,theta=pos(move[i],angle[i])
	x=x+new_x
	y=y+new_y
	
	coor_x.append(x)
	coor_y.append(y)

plt.plot(coor_x,coor_y)
plt.savefig("output.jpg")


	






