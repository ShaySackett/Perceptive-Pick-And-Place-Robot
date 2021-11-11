#!/usr/bin/env python3
from dorna2 import dorna
import rospy
import math
from std_msgs.msg import Int16 
from std_msgs.msg import UInt16
from std_msgs.msg import Bool

if __name__ == '__main__':

	rospy.init_node('hardcoded_dorna_demo')
	
	#create publishers for servo position and stepper motor steps
	stepperRun_pub = rospy.Publisher('/stepperRun', Int16, queue_size = 1)
	servo_pub = rospy.Publisher('/servo', UInt16, queue_size = 1)
	stepperENA_pub = rospy.Publisher('/stepperENA', Bool, queue_size = 1)
	rate = rospy.Rate(10)

	robot = dorna()
	ip = '10.33.6.1'
	port = 443
	robot.connect(ip, port)
	rospy.loginfo("Connected to Dorna!")

	loop_counter = 0

	while not rospy.is_shutdown():
		
		#if this is the first time the loop is running (else do nothing):
		if loop_counter == 0:
			servo_pos_msg = Int16()
			
			
			#open servo aperature to not collide with bolts when robot arm is lowered
			servo_pub.publish(15)
			
			#disable stepper to allow "free rotation" of stepper to allow bolt drive to drop into bolt head easier
			stepperENA_pub.publish(False)
			
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


			#start robot bolt demo routine, lower robot to first bolt position. 

			robot.play(cmd = "lmove", rel = 0, a = 0, b = 90, vel = 20, accel = 100,jerk = 1000, id = 1)
			robot.wait(id = 1, stat = 2)
			robot.play(cmd = "lmove", rel = 0, x = 354, y = 0, z = 150, vel = 20, accel = 100,jerk = 1000, id = 2)
			robot.wait(id = 2, stat = 2)
			robot.play(cmd = "lmove", rel = 0, z = 124, vel = 20, accel = 100,jerk = 1000, id = 3)
			robot.wait(id = 3, stat = 2)

			
			#enable stepper
			stepperENA_pub.publish(True)
			rospy.sleep(1)
			#rotate bolt ~6 times without lifting the z axis to allow aperture fingers to get under bolthead. 
			stepperRun_pub.publish(-800*7)
			#give time to unscrew bolt
			rospy.sleep(5)
			
			#Input servo angle here, in this case close servo	
			servo_pos_msg.data = 120
			servo_pub.publish(servo_pos_msg.data)
			rospy.sleep(3)
			
			#Variables for loop to unscrew bolt and raise z axis by equal amounts
			id_counter = 5
			new_z = 124

			for i in range(15): 
				#do 1 rotation of the stepper motor for each 1.25mm lift of robot arm (the pitch of 8mm screw)
				#rotate stepper motor once
				stepperRun_pub.publish(-800)
				#wait for stepper to rotate (yeah this whole code is kinda jank)
				rospy.sleep(1)
				#move dorna up by 1.25mm in z
				robot.play(cmd = "lmove", rel = 0, z = new_z + 1.25, vel = 1.25, accel = 100,jerk = 1000, id = id_counter)
				robot.wait(id = id_counter, stat = 2)
				#increase loop counter and robot arm id_counter
				i = i + 1
				id_counter = id_counter + 1
				rospy.loginfo(new_z)
				#set z height for next loop run to current z height  
				new_z = new_z + 1.25

			#move to travel z height
			robot.play(cmd = "lmove", rel = 0, z = 175, vel = 20, accel = 100,jerk = 1000, id = 100)
			robot.wait(id = 100, stat = 2)

			#intermediate moves to get robot to correct location
			robot.play(cmd = "jmove", rel = 0, j0 = .073, j1 = 170.361, j2 = -138.613, j3 = 55.260, j4 = 360.810, vel = 10, accel = 100,jerk = 1000, id = 101)
			robot.wait(id = 101, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j0 = 180.169, j1 = 168.669, j2 = -136.557, j3 = 61.256, j4 = 360.079, vel = 10, accel = 100,jerk = 1000, id = 102)
			robot.wait(id = 102, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j0 = 180, j1 = 119.493, j2 = 67.603, j3 = -5.513, j4 = 272.632, vel = 10, accel = 100,jerk = 1000, id = 103)
			robot.wait(id = 103, stat = 2)

			#move robot arm to other hole location
			robot.play(cmd = "lmove", rel = 0, x = 227.269, y = -1.764, vel = 10, accel = 100,jerk = 1000, id = 105)
			robot.wait(id = 105, stat = 2)
			robot.play(cmd = "lmove", rel = 0, a = 0, b = 90, vel = 20, accel = 100,jerk = 1000, id = 104)
			robot.wait(id = 104, stat = 2)
			robot.play(cmd = "lmove", rel = 0, z= 132, vel = 10, accel = 100,jerk = 1000, id = 106)
			robot.wait(id = 106, stat = 2)

			#tighten bolt
			id_counter = 200
			new_z = 132
			for i in range(10): 
				#do 1 rotation of the stepper motor for each 1.25mm drop of robot arm (the pitch of 8mm screw)
				#rotate stepper motor once
				stepperRun_pub.publish(800)
				#wait for stepper to rotate (yeah this whole code is kinda jank)
				rospy.sleep(1)
				#move dorna DOWN by 1.25mm in z
				robot.play(cmd = "lmove", rel = 0, z = new_z - 1.25, vel = 1.25, accel = 100,jerk = 1000, id = id_counter)
				robot.wait(id = id_counter, stat = 2)
				#increase loop counter and robot arm id_counter
				i = i + 1
				id_counter = id_counter + 1
				rospy.loginfo(new_z)
				#set z height for next loop run to current z height  
				new_z = new_z - 1.25
			
			
			
			
			#open aperature, set stepper speed to 0
			stepperRun_pub.publish(0)
			servo_pos_msg.data = 15
			servo_pub.publish(servo_pos_msg.data)
			rospy.sleep(5)

			
			robot.close()
			loop_counter = loop_counter + 1

		#no matter what open servo back up, make sure it isn't stalled
		rate.sleep()



	rospy.loginfo("Robot disconnected and node stopped")
	
