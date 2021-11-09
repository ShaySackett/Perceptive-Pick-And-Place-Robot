from dorna2 import dorna

if __name__ == '__main__':
	
	print("Here")
	#Start Robot from folded home position!
	
	robot = dorna()
	ip = '10.33.6.1'
	port = 443
	robot.connect(ip, port)
	print("connected!")

	#safe_startup
	robot.play(cmd = "jmove", rel = 0, j0 = 0, vel = 20, accel = 100,jerk = 1000, id = 1)
	robot.wait(id = 1, stat = 2)
	robot.play(cmd = "jmove", rel = 0, j3 = 0, vel = 20, accel = 100,jerk = 1000, id = 2)
	robot.wait(id = 2, stat = 2)
	robot.play(cmd = "jmove", rel = 0, j1 = 90, vel = 20, accel = 100,jerk = 1000, id = 3)
	robot.wait(id = 3, stat = 2)
	robot.play(cmd = "jmove", rel = 0, j2 = -60, vel = 20, accel = 100,jerk = 1000, id = 4)
	robot.wait(id = 4, stat = 2)
	robot.play(cmd = "jmove", rel = 0, j1 = 45, vel = 20, accel = 100,jerk = 1000, id = 5)
	robot.wait(id = 5, stat = 2)
	robot.play(cmd = "jmove", rel = 0, j1 = 0, j2 = 0, vel = 20, accel = 100,jerk = 1000, id = 6)
	robot.wait(id = 6, stat = 2)

	#robot_bolt_routine
	robot.play(cmd = "lmove", rel = 0, a = 0, b = 90, vel = 20, accel = 100,jerk = 1000, id = 1)
	robot.wait(id = 1, stat = 2)
	robot.play(cmd = "lmove", rel = 0, x = 354, y = 0, z = 150, vel = 20, accel = 100,jerk = 1000, id = 1)
	robot.wait(id = 1, stat = 2)
	robot.play(cmd = "lmove", rel = 0, z = 124, vel = 20, accel = 100,jerk = 1000, id = 3)
	robot.wait(id = 3, stat = 2)
	

	#Rotate and grab bolt with ROS serial then move robot up slightly( 1mm), probably repeat the process
	#robot.play(cmd = "lmove", rel = 0, z = 131, vel = 10, accel = 100,jerk = 1000, id = 4)
	#robot.wait(id = 4, stat = 2)

	robot.close()
	print("disconnected!")
	