import time 
import cv2
import numpy as np 
import datetime
import berryIMU as imu
import email01
#For the Raspberry pi pins
import RPi.GPIO as gpio 
import math 
import matplotlib.pyplot as plt
import imutils 
from picamera.array import PiRGBArray
from picamera import PiCamera
import os 
from threading import Thread as thread
global init_0
# init_0 = imu.get_vals()
file1 = open("move_data.txt","w+")
file2 = open("angle_data.txt","w+")
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

def distance(trig,echo):
	time.sleep(1)
	# avg_dist = []
	init()
	up = False
	down = False
	vlidate_val = False
	# for i in range(10)
	while vlidate_val != True:
		time.sleep(0.5)
		gpio.setmode(gpio.BOARD)
		gpio.setup(trig,gpio.OUT)
		gpio.setup(echo,gpio.IN)

		gpio.output(trig,False)
		time.sleep(0.01)
		#Generating the trigger pulse
		gpio.output(trig,True)
		time.sleep(0.00001)
		gpio.output(trig,False)
		while gpio.input(echo) == 0:
			up = True
			pulse_start = time.time()

		while gpio.input(echo) == 1:
			down = True
			pulse_stop = time.time()
		if up == True and down == True:
			pulse_duration = pulse_stop - pulse_start
			distance = round(pulse_duration*17150)
			vlidate_val = True
		else:
			distance = 0

	# 	avg_dist.append(distance)
	# distance = np.mean(avg_dist)
	gpio.cleanup()
	return distance
def tilt_compensation(intended):
	# curr = get_angle()
	if intended <= curr+5 or intended >= curr-5:
		print("correct turning")
		diff = 0
		stat = True
	else:
		diff = intended -curr
		if diff <0:
			right(-diff)
			stat = False
			# direc = 0
			print("Undershoot")
		elif diff >0:
			left(diff)
			stat = False
			# direc = 1
			print("Overshoot")

def reach_goal(a,b):
	print("Inside reach_goal")
	# global angles
	# curr_or = curr_angle_get()
	curr_or = get_cur_orr()
	distance  = ((a - 3.048)**2 + (b - 0.6096)**2)**0.5
	rads = math.atan2(b-0.6096,a-0.6096)
	deg = math.degrees(rads)
	# if curr_or > 180+deg:
	# 	turn_angle = (180-deg)+curr_or
	# elif curr_or < 180+deg
	# 	turn_angle = (180+deg)-curr_or
	return curr_or,distance

def goal_angle(a,b):
	distance  = ((a - 3.048)**2 + (b - 0.6096)**2)**0.5
	rads = math.atan2(b-0.6096,a-0.6096)
	deg = math.degrees(rads)
	deg = abs(deg)
	return deg,distance
# def get_angle():
# 	global init_0
# 	heading = imu.get_vals()
# 	new_angle = heading - init_0
# 	if new_angle <0:
# 		new_angle_out = new_angle +360
# 	else:
# 		new_angle_out = new_angle
# 	if new_angle_out >0 and new_angle_out <= 50:
# 		new_angle_out = new_angle_out*0.56
# 	elif new_angle_out > 50 and new_angle_out<=110:
# 		new_angle_out = new_angle_out *0.67
# 	elif new_angle_out > 110 and new_angle_out <= 220:
# 		new_angle_out = new_angle_out * 1.11
# 	elif new_angle_out >220 and new_angle_out <=360:
# 		new_angle_out = new_angle_out *1.56
# 	return new_angle_out

# def curr_angle_get():
# 	global angle
# 	curr_angle = np.sum(angle)
# 	if abs(curr_angle) >=360:
# 		if abs(curr_angle) >= 720:
# 			# curr_angle = abs(curr_angle)
# 			curr_angle_no = curr_angle /360
# 			if curr_angle >0:
# 				curr_angle = curr_angle - (360*curr_angle_no)
# 			else:
# 				curr_angle = curr_angle + (360*curr_angle_no)
# 	# curr_angle = abs(curr)
# 	# if curr_angle >0 and  curr_angle<:
# 		# curr_x,curr_y = directions(3,)
# 	return curr_angle
def add_angles(angle):
	vals = 0
	print("inside add angles")
	for i in range(len(angle)):
		# print(i)
		vals = int(angle[i])+vals
	return vals

def get_cur_orr():
	global angle
	print("inside curr_orientation",len(angle))
	# curr_angle = np.sum(angle)
	curr_angle = add_angles(angle)
	print("Finished Adding angles")
	if curr_angle>0:
		print("Angles are grater than 0")
		if curr_angle >=360:
			if curr_angle >= 720 or curr_angle >= 360:
				curr_angle_no = curr_angle/360
				curr_angle = curr_angle -(360*int(curr_angle_no))
	elif curr_angle < 0:
		if abs(curr_angle) >=360:
			if abs(curr_angle) >= 720 or abs(curr_angle) >= 360:
				curr_angle_no = curr_angle/360
				curr_angle = curr_angle + (360*int(curr_angle_no))
				# curr_angle = 360+curr_angle
		else:
			curr_angle = 360 + curr_angle
	print("Out of het_cur_orr")
	return curr_angle


def revs_ticks(final_dist):
	revs = (120/(2*math.pi* 0.0325)) * final_dist
	## for Ticks
	ticks = (960/(2*math.pi* 0.0325)) * final_dist
	return revs, ticks

def turn_angle(deg):
	circu = 2*math.pi*0.1007
	arc_lenght = (deg/360)*circu
	## revs calculation
	revs = (120/(2*math.pi* 0.0325)) * arc_lenght
	## Ticks Calculation
	ticks = (960/(2*math.pi* 0.0325)) * arc_lenght
	return revs, ticks

def pos(l,theta):
	vals = theta*(3.14/180)
	new_x = l*(math.cos(vals))
	new_y = l*(math.sin(vals))
	return new_x,new_y,theta

def forward(inp):
	init()
	# Left wheels 
	pwm1 = gpio.PWM(31,50)
	# Right Wheels
	pwm2= gpio.PWM(37,50)
	val = 30
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'w')
	# print("Moved Forward")

def reverse(inp):
	init()
	#Left Reverse Wheels
	pwm1 = gpio.PWM(33,50)
	#Right Reverse Wheels
	pwm2= gpio.PWM(35,50)
	val = 30
	#distance = inp
	final_dist,final_ticks = revs_ticks(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'s')
	# print("Moved Backward")

def right(inp):
	init()
	pwm1 = gpio.PWM(31,50)
	pwm2= gpio.PWM(35,50)
	val = 70
	#distance = inp
	final_dist,final_ticks = turn_angle(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'d')
	# print("Moved Right")

def left(inp):
	init()
	pwm1 = gpio.PWM(33,50)
	pwm2= gpio.PWM(37,50)
	val = 70
	#distance = inp
	final_dist,final_ticks = turn_angle(inp)
	execute(inp,pwm1,pwm2,val,final_ticks,'a')
	# print("Moved Left")

def openg():
	gpio.setmode(gpio.BOARD)
	gpio.setup(36, gpio.OUT)
	pwm = gpio.PWM(36, 50)
	pwm.start(5)
	pwm.ChangeDutyCycle(9.5)
	time.sleep(1)

def closeg():
	gpio.setmode(gpio.BOARD)
	gpio.setup(36, gpio.OUT)
	pwm = gpio.PWM(36, 50)
	pwm.start(5)
	pwm.ChangeDutyCycle(3.5)
	time.sleep(1)

def update_curr(curr_x,curr_y,length,theta):

	n_x= length*(math.cos(theta*(3.14/180)))
	n_y= length*(math.sin(theta*(3.14/180)))
	
	curr_x = curr_x+n_x
	curr_y = curr_y+n_y
	#print("The new x and y",curr_x,curr_y)
	return curr_x,curr_y


def em(curr_x,curr_y):
	# curr_x = curr_x
	curr_x = meter_to_inches(curr_x)
	# curr_y = curr_y - 1
	curr_y = meter_to_inches(curr_y)
	email01.mail(curr_x,curr_y)
	# cmd = 'python3 email01.py'
	# os.system(cmd)

##Change the values to the new values from final program
def execute(distance,pwm1,pwm2,val,final_ticks,event):
	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0) 
	dist = 0
	final_dist = distance
	if event == "a":
		# Final Values to the PWM for forward
		pwm1.start(val)
		pwm2.start(val+0.002)	
	elif event == 's':
		pwm1.start(val)
		#pwm2.start(val+62)
		pwm2.start(val)
	
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

def camera():
	camera = PiCamera()
	camera.rotation = 180
	rawCapture = PiRGBArray(camera, size=(640,480))
	camera.resolution = (640,480)
	camera.start_preview() 
	time.sleep(2)
	camera.capture(rawCapture,format = 'bgr')
	camera.stop_preview()
	image =rawCapture.array
	# image = cv2.flip(image,-1)
	# if red == False or blue == False:
	inp = input("The color to pick: ")
	# inp = '1g'
	if inp == 'r':
		print("Searching Red")
		lower_red= np.array ([0,75,120])
		upper_red = np.array([5,255,255])
	if inp == 'b':
		print("Searching blue")
		lower_red= np.array ([98,179,88])
		upper_red = np.array([120,255,231])
	if inp == 'g':
		print("Searching green")
		cv2.imwrite('image.jpg',image)
		lower_red = np.array([55,124,31])
		upper_red= np.array ([98,255,255])
	# if red == True and blue == False
	# elif red == True and blue == False:
		# lower_blue = ([100,50,65]) 
		# upper_blue =  ([130,100,200])

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask= cv2.inRange(hsv,lower_red,upper_red)
	result=cv2.bitwise_and(hsv, hsv, mask=mask)
	blur = cv2.GaussianBlur(mask,(9,9),0)
	cv2.imwrite("mask.jpg",mask)
	cv2.imwrite('hsv.jpg',hsv)
	cv2.imwrite('result.jpg',result)
	cv2.drawMarker(image,(320,240),1 )
	ret,thresh = cv2.threshold(blur,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(image, contours, -1, (0,0,255), 3)
	# Find the index of the largest contour
	areas = [cv2.contourArea(c) for c in contours]
	if areas != []:
		camera_stat = True
		max_index = np.argmax(areas)
		cnt=contours[max_index]
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		print("the x and y values are ",x,y)
		center = (int(x),int(y))
		radius=int(radius)

	else:
		camera_stat = False
		x = None 
		y = None
	camera.close()
	return x,y,camera_stat

def directions(event,inp,curr_x,curr_y):
	if event ==1 :
		forward(inp)
		inp_temp = meter_to_inches(inp)
		move.append(inp_temp)
		angle.append(0)
		if len(angle) != 1:
			curr_x_temp,curr_y_temp = update_curr(curr_x,curr_y,inp,(angle[len(angle)-1]+angle[len(angle)-2]))
		else:
			curr_x_temp,curr_y_temp = update_curr(curr_x,curr_y,inp,(angle[0]))
	elif event ==2:
		reverse(inp)
		inp_temp = meter_to_inches(inp)
		move.append(-inp_temp)
		angle.append(0)
		if len(angle) != 1:
			curr_x_temp,curr_y_temp = update_curr(curr_x,curr_y,-inp,(angle[len(angle)-1]+angle[len(angle)-2]))
		else:
			curr_x_temp,curr_y_temp = update_curr(curr_x,curr_y,-inp,(angle[0]))
	elif event ==3:
		left(inp)
		move.append(0)
		angle.append(inp)
		curr_x_temp,curr_y_temp = update_curr(curr_x,curr_y,0,inp)
	else:
		right(inp)
		move.append(0)
		angle.append(-inp)
		curr_x_temp,curr_y_temp = update_curr(curr_x,curr_y,0,-inp)
	return curr_x_temp,curr_y_temp

# y = 1x = 1
move_counter = 0
move_encoder = []
move_IMU = []
coor_x = []
coor_y = []
#current value as global
curr_x = 0.3048
curr_y = 0.3048
global angle,move
angle = []
move = []

obj_stat = False


def turn_to_object(x,y,curr_x,curr_y):
	print("inside the turn to object ",x,y)
	degblock=0
	# time.sleep
	if x>340:
		degblock= (x-640/2)*0.061
		curr_x,curr_y = directions(4,degblock,curr_x,curr_y)
		# right(degblock)
	if x<290:
		degblock=abs((x-(640/2))*0.061)
		curr_x,curr_y = directions(3,degblock,curr_x,curr_y)
		# left(degblock)
	time.sleep(1)
	
	print("The value of x is",x,y)
	gpio.cleanup()
	if x>280 and x<350:
		print("Going into movement function")
		pick_stat,curr_x,curr_y = movement(curr_x,curr_y,x,y)
	else:
		print("Repeating the else function for turn_to_object")
		main(curr_x,curr_y,False,0)
	return curr_x,curr_y
		
# def validate(dist):
# 	if dist == 0:
# 		dirt_val = True
# 	else:
# 		dirt_val = False
# 	return dirt_val
## Checks for placement of the robot when near the wall
def wall_side():
	#front top ultrasonic sensor
	dist1 = distance(11,38)
	#front left ultrasonic sensor
	dist2 = distance(13,40)

	if dist1 > 25:
		direction = 1
	elif dist2 > 25:
		direction  = 2
	else:
		direction = 3
	return direction

def object_check(curr_x,curr_y,object_pick_stat):
	dist1 = distance(13,40)
	print("Indside Obstacle Checks")

	if dist1 < 25:
		print("Collision avoidance")
		curr_x,curr_y = directions(3,90,curr_x,curr_y)
		dist2 = distance(11,38)
		while dist2 < 20:
			curr_x,curr_y = directions(1,0.1,curr_x,curr_y)
			dist2 = distance(11,38)
		if object_pick_stat == True:
			go_to_finish(curr_x,curr_y)
		else:
			main(curr_x,curr_y,object_pick_stat,0)
			# obj_stat = False
	return curr_x,curr_y,object_pick_stat
#TODO Use the stat to block out some part of the trajectories in the movement
def collision_check(curr_x,curr_y,obj_stat):
	if curr_x < 0.8 or curr_x > 11  or curr_y > 11 or curr_y < 0.8:
		wall_stat = True
		side = wall_side()
	else:
		wall_stat = False
	time.sleep(0.2)
	dist1 =distance(16,18)
	# time.sleep(1)
	dist2 = distance(11,38)
	# time.sleep(1)
	dist3 = distance(13,40)
	if dist1 > 25 and dist2 >25 and dist3 >25:
		wall_stat = False
	else:
		curr_x,curr_y,wall_stat = object_check(curr_x,curr_y,obj_stat)
	return curr_x,curr_y,wall_stat


def cm_to_meter(inp):
	dist_temp = inp/100
	#final_dist = meter_to_inches(dist_temp)
	return dist_temp

def meter_to_inches(inp):
	dist_temp = inp*39.37
	return dist_temp
#TODO
def search_obj(curr_x,curr_y,move_counter):
	print("Searching for the object",move_counter)
	if move_counter <8:
		# left(90)
		curr_x,curr_y = directions(3,45,curr_x,curr_y)
		# tilt_compensation(270-(90*counter))
		move_counter +=1
		main(curr_x,curr_y,False,move_counter)
	else:
		print("Going toward a region")
		curr_x,curr_y = directions(1,0.2,curr_x,curr_y)
		# forward(0.2)
		move_counter = 0
	# curr_x,curr_y = directions(1,0.25,curr_x,curr_y)
	# curr_x,curr_y = directions(3,90,curr_x,curr_y)
	# main(curr_x,curr_y,False,move_counter)
	return curr_x,curr_y,move_counter



# #Forward Movement of the Robot
# def  go_to_finish(curr_x,curr_y):
# 	home_x = 2
# 	home_y = 10
# 	print("Going to the finish line",curr_x,curr_y)
# 	while curr_x > 4 and curr_y <8:
# 		#Front top senor reading
# 		collision_dist = distance(13,40)
# 		if collision_dist > 15:
# 			distance  = math.sqrt((curr_x-home_x)**2+(curr_y - home_y)**2)
# 			slope = (curr_y - home_y)/(curr_x - home_x)
# 			angle = math.atan(slope)
# 			angle = math.degrees(angle)
# 			if angle < 0 :
# 				curr_x,curr_y = directions(3,angle,curr_x,curr_y)
# 				curr_x,curr_y = directions(1,distance/2,curr_x,curr_y)
# 				# left(angle)
# 				# forward(distance)
# 			elif angle > 0:
# 				curr_x,curr_y = directions(4,angle,curr_x,curr_y)
# 				curr_x,curr_y = directions(1,distance/2,curr_x,curr_y)
# 			# right(angle)
# 			# forward(distance)
# 		else:
# 			#go to collision detection
# 			curr_x,curr_y,collision_stat = collision_check(curr_x,curr_y)
# 	object_pickup = False
# 	return curr_x,curr_y,object_pickup

# def go_to_finish(curr_x,curr_y):
# 	angle = get_angle()
# 	intended_angle = 185
# 	diff = angle - intended_angle
# 	print("Going to the drop off zone",angle,diff)
# 	if angle > 0:
# 		print("Turning towards the wall")
# 		curr_x,curr_y = directions(4,diff,curr_x,curr_y)
# 		tilt_compensation(intended_angle)
# 	else:
# 		curr_x,curr_y = directions(3,abs(diff),curr_x,curr_y)
# 	dist = distance(13,40)
# 	dist = cm_to_meter(dist)
# 	curr_x,curr_y = directions(1,dist-0.2,curr_x,curr_y)
# 	angle_temp = get_angle()
# 	intended_angle = 90
# 	intended_angle_temp = 80
# 	diff_temp = angle- intended_angle
# 	diff_temp1 = angle - intended_angle_temp
# 	if diff_temp > 0:
# 		curr_x,curr_y = directions(3,diff_temp,curr_x,curr_y)
# 		current_angle = get_angle()
# 		if current_angle > 0 and current_angle < 95:
# 			tilt_compensation(intended_angle)
# 		elif current_angle >180 and current_angle < 360:
# 			tilt_compensation(intended_angle_temp)
# 	dist = distance(13,40)
# 	dist = cm_to_meter(dist)
# 	curr_x,curr_y = directions(1,dist -0.2,curr_x,curr_y)
# 	closeg()
# 	curr_x,curr_y = directions(2,0.1,curr_x,curr_y)
# 	return curr_x,curr_yp
def go_to_ref(curr_x,curr_y,angle_ref):
	print("Going to reference position",angle_ref)
	if angle_ref >=0 and angle_ref < 180:
		print("Going to ref position 90")
		if angle_ref >90:
			angle_diff = angle_ref - 90
			# curr_x,curr_y = directions(3,90,curr_x,curr_y)
			curr_x,curr_y = directions(4,angle_diff,curr_x,curr_y)
			time.sleep(0.2)
		else:
			curr_x,curr_y = directions(3,90-angle_ref,curr_x,curr_y)
			time.sleep(0.2)
		# curr_x,curr_y = directions(3,90,curr_x,curr_y) 
	elif angle_ref<=270 and angle_ref>=180:
		angle_temp = 270 - angle
		curr_x,curr_y = directions(3,angle_temp,curr_x,curr_y)
		time.sleep(0.2)
		curr_x,curr_y = directions(3,92,curr_x,curr_y)
		time.sleep(0.2)
		curr_x,curr_y = directions(3,92,curr_x,curr_y)
		time.sleep(0.2)
	elif angle_ref >270 and angle_ref <360:
		angle_temp = 360-angle_ref
		curr_x,curr_y = directions(3,angle_temp,curr_x,curr_y)
		time.sleep(0.2)
		curr_x,curr_y = directions(3,90,curr_x,curr_y)
		time.sleep(0.2)
	print("Exitting from ref pos")
	return curr_x,curr_y

def go_to_finish(curr_x,curr_y):
	curr_x = float(curr_x)
	curr_y = float(curr_y)
	angle_finish,distan = reach_goal(curr_x,curr_y)
	print("Going to reference angle from", angle_finish,distan)
	curr_x,curr_y = go_to_ref(curr_x,curr_y,angle_finish)
	dist = distance(13,40)
	# print()
	dist = cm_to_meter(dist)
	curr_x,curr_y = directions(1,dist-0.5,curr_x,curr_y)
	time.sleep(0.2)
	curr_x,curr_y = directions(3,90,curr_x,curr_y)
	time.sleep(0.2)
	dist = distance(13,40)
	dist = cm_to_meter(dist)
	curr_x,curr_y = directions(1,dist-0.5,curr_x,curr_y)
	openg()
	curr_x,curr_y = directions(2,0.2,curr_x,curr_y)
	return curr_x,curr_y

# def go_to_finish(curr_x,curr_y):
# 	print("Going to Drop off Zone")
# 	# angle_finish = get_angle()
# 	# print(curr_x.type(),curr_y.type())
# 	curr_x = float(curr_x)
# 	curr_y = float(curr_y)
# 	angle_finish,distan = reach_goal(curr_x,curr_y)
# 	print("Going to reference angle from", angle_finish,distan)
# 	curr_x,curr_y = go_to_ref(curr_x,curr_y,angle_finish)
# 	# home_x = 2
# 	# home_y = 10
# 	# distance  = math.sqrt((curr_x-home_x)**2+(curr_y - home_y)**2)
# 	# slope = (curr_y - home_y)/(curr_x - home_x)
# 	# theta = math.atan(slope)
# 	# theta = math.degrees(theta)
# 	# curr_angle = get_angle()
# 	angle_finish,distan = goal_angle(curr_x,curr_y)
# 	if angle_finish > 10:
# 		print("Angle les than 10",angle_finish)
# 		curr_x,curr_y = directions(3,angle_finish-5,curr_x,curr_y)
# 	else:
# 		print("angle greater than 10",angle_finish)
# 		curr_x,curr_y = directions(3,angle_finish,curr_x,curr_y)
# 	time.sleep(0.2)
# 	dist = distance(13,40)
# 	if dist < distan:
# 		curr_x,curr_y = directions(1,dist,curr_x,curr_y)
# 	else:
# 		curr_x,curr_y = directions(1,distan,curr_x,curr_y)
# 	time.sleep(0.2)
# 	dist = distance(13,40)
# 	# curr_x,curr_y = directions(1,0.2,curr_x,curr_y)
# 	# _,distance_2 = reach_goal(curr_x,curr_y)
# 	# distance_2 =  math.sqrt((curr_x-home_x)**2+(curr_y - home_y)**2)
# 	# curr_x,curr_y = directions(1,distance_2-0.05,curr_x,curr_y)
# 	# time.sleep(0.2)
# 	openg()
# 	em(curr_x,curr_y)
# 	time.sleep(0.1)
# 	curr_x,curr_y = directions(2,0.2,curr_x,curr_y)
# 	return curr_x,curr_y

def movement(curr_x,curr_y,x,y):
	# print("Current point in movement",curr_x,curr_y)
	dist = distance(16,18)
	dist1 = distance(13,40)
	print("Current point in movement",curr_x,curr_y,dist1,dist)
	dist_in = cm_to_meter(dist)
	if dist1 > dist:
		print("The object is correct")
		curr_x,curr_y = directions(1,dist_in-0.15,curr_x,curr_y)
		if dist_in > 1:
			curr_x,curr_y = directions(1,0.1,curr_x,curr_y)
			print("The distance is more than 1")
			main(curr_x,curr_y,False,0)
		# forward(dist-15)
		# print
		openg()
		dist_temp = distance(16,18)
		print("The new distance from the object is",dist_temp)
		if 6<= dist_temp <=25:
			print("picking up object")
			openg()
			dist_temp_in = cm_to_meter(dist_temp)
			curr_x,curr_y = directions(1,abs(dist_temp_in)+0.1,curr_x,curr_y)
			# forward(0.02)
			closeg()
			em(curr_x,curr_y)
			curr_x,curr_y = go_to_finish(curr_x,curr_y)
			# curr_x,curr_y = directions(3,90,curr_x,curr_y)
			time.sleep(0.1)
			# curr_x,curr_y = d,irections(3,90,curr_x,curr_y)
			# red_up.append(1)
			# blue.append(1)
		elif dist_temp > 25:
			main(curr_x,curr_y,False,0)
			print("Object a bit far off moving forward and picking it up")
			dist_temp_in = cm_to_meter(dist_temp)
			openg()
			curr_x,curr_y = directions(1,dist_temp_in+0.1,curr_x,curr_y)
			time.sleep(0.5)
			closeg()
			curr_x,curr_y = go_to_finish(curr_x,curr_y)
			time.sleep(0.2)
		else:
			print("Assuming it picked up the object")
	object_pickup = False
	print("exitting object pickup")
	return object_pickup,curr_x,curr_y

def turn_180(curr_x,curr_y):
	print("taking the 180 degree turn")
	curr_x,curr_y = directions(3,90,curr_x,curr_y)
	# tilt_compensation(270)
	time.sleep(0.1)
	curr_x,curr_y = directions(3,90,curr_x,curr_y)
	# tilt_compensation(270-45)
	return curr_x,curr_y

def main(curr_x,curr_y,obj_stat,counter):
	init()
	# global counter
	print("curr values",curr_x,curr_y,'objstat',obj_stat)
	curr_x,curr_y,collision_stat = collision_check(curr_x,curr_y,obj_stat)
	if collision_stat == False:
		x,y,camera_stat = camera()
		print("the camera_state is",camera_stat)
		if camera_stat == True:
			curr_x,curr_y = turn_to_object(x,y,curr_x,curr_y)
			# curr_x,curr_y = go_to_finish(curr_x,curr_y)
			matplot(curr_x,curr_y,0)

			# curr_x,curr_y = go_to_finish(curr_x,curr_y)
			# gameover()
			
		elif camera_stat == False:
			curr_x,curr_y,counter = search_obj(curr_x,curr_y,0+counter)
			counter = main(curr_x,curr_y,False,counter)
	else:
		print("Collision immenent")
	return counter

def matplot(curr_x,curr_y,counter):
	global move, angle
	print("plotting map",len(move),len(angle))
	plot(move,angle)
	# plt.plot(move,angle)
	# plt.savefig("path.jpg")
	curr_x,curr_y = turn_180(curr_x,curr_y)
	main(curr_x,curr_y,False,counter)

def plot(move,angle):
	x = 1 
	y = 1
	coor_x = []
	coor_y = []
	for i in range(0,len(move)-1):
		out_vals1 = str(move[i])+"\n"
		out_vals2 = str(angle[i])+"\n"
		file1.write(out_vals1)
		file2.write(out_vals2)
		angle[i] = angle[i]+angle[i+1]
		new_x,new_y,theta = pos(move[i],angle[i])
		x = x+new_x
		y = y+new_y
		coor_x.append(x)
		coor_y.append(y)
	plt.plot(coor_x,coor_y)
	plt.savefig("path.jpg")

counter = 0
if __name__ == '__main__':
	while True:
		counter = main(curr_x,curr_y,obj_stat,counter)







	





