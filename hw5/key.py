#import os
#import event
import time

def key_init(event):
	print("key :",event)
	tf = 1

	if event.lower() == 'w':
		print("Forward")
	elif event.lower() == 's':
		print("Backward")
	elif event.lower() == 'a':
		print("Left")
	elif event.lower() == 'd':
		print("Right")
	else:
		print("Wrong Keys press 'w','a','s','d', or 'p' to quit")


while True:
	key_input = input("Select Driving Keys :")
	if key_input == "p":
		break
	key_init(key_input)


