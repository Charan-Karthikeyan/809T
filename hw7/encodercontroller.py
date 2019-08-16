import RPi.GPIO as gpio
import numpy as np

##initalize GPIO pins ###
def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)
	#gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)

def gameover():
	gpio.output(31,False)
	gpio.output(33,False)
	gpio.output(35,False)
	gpio.output(312,False)

	gpio.cleanup()

# Main code#
init()
counter = np.uint64(0)
# counter1 = np.uint64(0)
button = int(0)
#pwm1 = gpio.PWM(312,50)
#val = 20
#pwm1.start(val)
#time.sleep()
# button1 = int(0)
while True:
	if int(gpio.input(12))!= int(button):
		button = int(gpio.input(12))
		counter +=1
		print(counter)

	# if int(gpio.input(12))!= int(button1):
	# 	button1 = int(gpio.input(12))
	# 	counter1 +=1
	# 	print("the counter value ",counter1)

	if counter >= 960:
		gameover()
		print("Finished Game")
		break


