import RPi.GPIO as gpio
import time
import numpy as np 
from matplotlib import pyplot as plt

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

## Main Code ##

init()
counterBR = np.uint64(0)
counterFL = np.uint64(0)

buttonBR = int(0)
buttonFL = int(0)

pwm1= gpio.PWM(35,50)
pwm2 = gpio.PWM(31,50)
val = 20
pwm1.start(val)
pwm2.start(val)
time.sleep(0.1)

for i in range(0,1000000):
	print("counterBR", counterBR,"counterFL",counterFL,"BR state :",gpio.input(12),"FL State",gpio.input(7))
	file.write(str(gpio.input(12))+"\n")
	file1.write(str(gpio.input(7))+"\n")

	if int(gpio.input(12)) != int(buttonBR):
		buttonBR = int(gpio.input(12))
		counterBR += 1

	if int(gpio.input(7)) != int(buttonFL):
		buttonFL = int(gpio.input(7))
		counterFL += 1
		
	if counterBR >= 960:
		pwm1.stop()
		#gameover()
		#stop_time = time.time()
		#final_time = stop_time-start_time
		print("Game Over BR")
		#file.close()
		#break
	if counterFL >= 950:
		pwm2.stop()
		print("Game Over FL")
	if counterFL >=950 and counterBR >=960:
		gameover()
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