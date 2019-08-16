import RPi.GPIO as gpio
import time
import numpy as np
import matplotlib.pyplot as plt

file  = open("gpio_out.txt","w+")
#INIT FUNCTION ##
def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(31,gpio.OUT)
	gpio.setup(33,gpio.OUT)
	gpio.setup(35,gpio.OUT)
	gpio.setup(37,gpio.OUT)

	gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)

def gameover():
	gpio.output(31,False)
	gpio.output(33,False)
	gpio.output(35,False)
	gpio.output(37,False)

	gpio.cleanup()

## Main Code ##

init()
start_time = time.time()
counter  = np.uint64(0)
button = int(0)

#initalize pwm signal

pwm = gpio.PWM(31,50)
val = 20
pwm.start(val)
time.sleep(0.1)

for i in range(0,1000000):
	print("The counter is", counter,"and the GPIO state :",gpio.input(12))
	file.write(str(gpio.input(12))+"\n")

	if int(gpio.input(12)) != int(button):
		button = int(gpio.input(12))
		
		counter += 1
	if counter >= 960:
		pwm.stop()
		gameover()
		stop_time = time.time()
		final_time = stop_time-start_time
		print("Game Over",final_time)
		file.close()
		break

state = np.genfromtxt("gpio_out.txt")
plt.plot(state,"r-*")
plt.xlabel("GPIO Input Reading")
plt.ylabel("Encoder State")
plt.title("Motor Encoder Ananlysis")
plt.show()