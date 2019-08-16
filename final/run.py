import berryIMU as imu
global init_0
init_0 = imu.get_vals()

def get_angle():
	global init_0
	heading = imu.get_vals()
	new_angles = heading - init_0
	if new_angles <0:
		new_angle_out = new_angles +360
	else:
		new_angle_out = new_angles

	if new_angle_out >0 and new_angle_out <= 50:
		print("between 0 and 50",new_angle_out)
		new_angle_out = new_angle_out*0.56
	elif new_angle_out > 50 and new_angle_out<=110:
		print("Between 50 and 110",new_angle_out)
		new_angle_out = (new_angle_out - 50)
		new_angle_out = (new_angle_out *0.67)+50
	elif new_angle_out > 110 and new_angle_out <= 220:
		print("Between 110 and 220",new_angle_out)
		new_angle_out = (new_angle_out - 110)
		new_angle_out = (new_angle_out *1.11)+110
		# new_angle_out = new_angle_out * 1.11
	elif new_angle_out >220 and new_angle_out <=360:
		print("Between 220 and 360",new_angle_out)
		# new_angle_out = new_angle_out *1.56
		new_angle_out = (new_angle_out - 220)
		new_angle_out = (new_angle_out *1.56)+220
	return new_angle_out

for i in range(100):
	a = get_angle()
	print(a)
# orig_heading = imu.get_vals()
# for i in range(100000):
# 	if i == 0:
# 		print("getting")
# 		init_0 = imu.get_vals()
# 	heading = imu.get_vals()
# 	new_angles =  heading - init_0
# 	if new_angles <0:
# 		new_angles = new_angles +360
# 	print("The new _angles are ",new_angles,"and the heading is",heading,"init readings are ",init_0)