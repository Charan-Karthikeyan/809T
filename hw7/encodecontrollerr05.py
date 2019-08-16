import RPi.GPIO as gpio
import time
import numpy as np 
from matplotlib import pyplot as plt
import math

file  = open("BR_out.txt","w+")
file1 = open("FL_out.txt","w+")
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
# def revs_to_distance(final_dist):
# 	revs = final_dist/(39.36*2*math.pi*0.0325)
# 	return revs

# def revs_to_ticks(final_dist):
# 	revs = final_dist/(39.36*2.math/pi*0.0325)
# 	ticks  = revs * 955                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
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

## Main Code ##

init()
counterBR = np.uint64(0)
counterFL = np.uint64(0)

buttonBR = int(0)
buttonFL = int(0)
#have to change this for direction control
# pwm2 = gpio.PWM(35,50)
# pwm1= gpio.PWM(33,50)
pwm2 = gpio.PWM(31,50)
pwm1= gpio.PWM(35,50)
val = 60
pwm1.start(val)
pwm2.start(val)
time.sleep(0.1)
diatance = 0
final_dist = 1

# if event.lower() == 'w' or event.lower() == 's':
# 	final_rev,final_ticks = revs_ticks(final_dist)	
# 	if event.lower() == 'w':
# 		pwm1= gpio.PWM(31,50)
# 		pwm2 = gpio.PWM(37,50)
# 	elif event.lower() == 's':
# 		pwm1= gpio.PWM(33,50)
# 		pwm2 = gpio.PWM(35,50)
# else event.lower() == 'a' or event.lower() == 'd':
# 	final_rev,final_ticks = turn(90)
# 	if event.lower() == 'a':
# 		pwm1= gpio.PWM(31,50)
# 		pwm2 = gpio.PWM(35,50)
# 	elif event.lower() == 'd':
# 		pwm1= gpio.PWM(33,50)
# 		pwm2 = gpio.PWM(37,50)
final_rev,final_ticks = turn(90)
counterFL_final = np.uint64(0)
counterBR_final = np.uint64(0)
rev_counter  = 0
def key_init(event):
	init()


print(final_rev,final_ticks)
for i in range(0,10000000):
	# key_input = input("Select Driving Keys :")
	#if 
	print("counterBR", counterBR,"counterFL",counterFL,"BR state :",gpio.input(12),"FL State",gpio.input(7))
	print("The final Ticks",final_ticks)
	
	if int(gpio.input(12)) != int(buttonBR):
		buttonBR = int(gpio.input(12))
		counterBR += 1
		counterBR_final +=1

	if int(gpio.input(7)) != int(buttonFL):
		buttonFL = int(gpio.input(7))
		counterFL += 1
		counterFL_final +=1
		
	# if counterBR >= 960:
	# 	pwm1.stop()
	# 	#gameover()
	# 	#stop_time = time.time()
	# 	#final_time = stop_time-start_time
	# 	print("Game Over BR")
	# 	#file.close()
	# 	#break
	# if counterFL >= 950:
	# 	pwm2.stop()
	# 	print("Game Over FL")
	#if counterFL >=950 and counterBR >=960:
	
	if counterFL < counterBR:
		print("change in br")
		pwm2.ChangeDutyCycle(val+5)
	if counterFL > counterBR:
		print("change in fl ")
		pwm1.ChangeDutyCycle(val+5)


	if counterFL_final >= final_ticks and counterBR_final >= final_ticks :
		print("Travelled",final_dist,"Inches")
		break
		


		

#state = np.genfromtxt("BR_out.txt")
#state1 = np.genfromtxt("FL_out.txt")
# plt.plot(state,"b-*")
# plt.xlabel("GPIO Input Reading")
# plt.ylabel("BR Encoder State")
# plt.title("Motor Encoder Ananlysis")
# plt.plot(state1,"r-*")
# plt.ylabel("FR encoder State")
# plt.xlabel("GPIO input Reading")
# plt.show()

# ax1 = plt.subplot(2,2,1)
# ax2 = plt.subplot(2,2,2)

# plt.subplot()
# f,ax_arr = plt.subplots(2,sharex = True)
# ax_arr[0].plot(state)
# ax_arr[0].set_ylabel("BR Encoder State")
# ax_arr[0].set_title("Motor Control Ananlysis")
# ax_arr[1].plot(state1)
# ax_arr[1].set_ylabel("FL Encoder State")
# ax_arr[1].set_xlabel("GPIO Reading")
# plt.show()