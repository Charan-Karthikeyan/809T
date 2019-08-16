import time
import RPi.GPIO as gpio

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(31,gpio.OUT) # in1
	gpio.setup(33,gpio.OUT) # in2
	gpio.setup(35,gpio.OUT) # in3
	gpio.setup(37,gpio.OUT) # in4

def game_stop():
	#Setting all the pins to low
	gpio.output(31,False)
	gpio.output(33,False)
	gpio.output(35,False)
	gpio.output(37,False)

def forward(tf):
	init()
	print("Forward")
	#For the left wheels
	gpio.output(31,True)
	gpio.output(33,False)
	#For the right wheels
	gpio.output(35,False)
	gpio.output(37,True)
	# Wait
	time.sleep(tf)
	#Stop all execution
	game_stop()
	#print("stopping")
	gpio.cleanup()

def right(tf):
	init()
	print("Right")
	#For the left wheels
	gpio.output(31,True)
	gpio.output(33,False)
	#For the right wheel
	gpio.output(35,True)
	gpio.output(37,False)
	#wait
	time.sleep(tf)
	#stop and cleanup
	game_stop()
	#print("Stopping")
	gpio.cleanup()

def left(tf):
	init()
	print("Left")
	#For the left wheels
	gpio.output(31,False)
	gpio.output(33,True)
	#For the right wheel
	gpio.output(35,False)
	gpio.output(37,True)
	#wait
	time.sleep(tf)
	#stop and cleanup
	game_stop()
	#print("Stopping")
	gpio.cleanup()

def reverse(tf):
	init()
	print("Reverse")
	#For the left wheels
	gpio.output(31,False)
	gpio.output(33,True)
	#For the right wheel
	gpio.output(35,True)
	gpio.output(37,False)
	#wait
	time.sleep(tf)
	#stop and cleanup
	game_stop()
	#print("Stopping")
	gpio.cleanup()

def key_init(event):
	init()
	print("key :",event)
	tf = 1

	if event.lower() == 'w':
		# print("Forward")
		forward(tf)
	elif event.lower() == 's':
		# print("Backward")
		reverse(tf)
	elif event.lower() == 'a':
		# print("Left")
		left(tf)
	elif event.lower() == 'd':
		# print("Right")
		right(tf)
	else:
		print("Wrong Keys press 'w','a','s','d', or 'p' to quit")


while True:
	key_input = input("Select Driving Keys :")
	if key_input == "p":
		break
	key_init(key_input)