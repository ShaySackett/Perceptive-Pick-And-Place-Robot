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

			robot.play(cmd = "jmove", rel = 0, j0 = 0, vel = 40, accel = 100,jerk = 1000, id = 1)
			robot.wait(id = 1, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j3 = 0, vel = 40, accel = 100,jerk = 1000, id = 2)
			robot.wait(id = 2, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j1 = 90, vel = 40, accel = 100,jerk = 1000, id = 3)
			robot.wait(id = 3, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j2 = -60, vel = 40, accel = 100,jerk = 1000, id = 4)
			robot.wait(id = 4, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j1 = 45, vel = 40, accel = 100,jerk = 1000, id = 5)
			robot.wait(id = 5, stat = 2)
			robot.play(cmd = "jmove", rel = 0, j1 = 0, j2 = 0, vel = 40, accel = 100,jerk = 1000, id = 6)
			robot.wait(id = 6, stat = 2)


			#start robot bolt demo routine, lower robot to first bolt position.

			z_start_height = 122 

			#bolt position #1
			robot.play(cmd = "lmove", rel = 0, a = 0, b = 90, vel = 40, accel = 100,jerk = 1000, id = 1)
			robot.wait(id = 1, stat = 2)
			robot.play(cmd = "lmove", rel = 0, x = 354, y = -2, z = 150, vel = 40, accel = 100,jerk = 1000, id = 2)
			robot.wait(id = 2, stat = 2)
			robot.play(cmd = "lmove", rel = 0, z = z_start_height, vel = 40, accel = 100,jerk = 1000, id = 3)
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
			new_z = z_start_height

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
			robot.play(cmd = "lmove", rel = 0, z = 175, vel = 40, accel = 100,jerk = 1000, id = 100)
			robot.wait(id = 100, stat = 2)

			#move robot arm to other hole location
			z_tighten_height = 135

			robot.play(cmd = "lmove", rel = 0, a = 1, b = 91, vel = 40, accel = 100,jerk = 1000, id = 104)
			robot.wait(id = 104, stat = 2)
			robot.play(cmd = "lmove", rel = 0, x = 420, y = 17, vel = 20, accel = 100,jerk = 1000, id = 105)
			robot.wait(id = 105, stat = 2)
			robot.play(cmd = "lmove", rel = 0, z = z_tighten_height, vel = 20, accel = 100,jerk = 1000, id = 106)
			robot.wait(id = 106, stat = 2)

			#tighten bolt
			id_counter = 200
			new_z = z_tighten_height
			
			open_servo_previously = False   #variable to make sure servo and delay for servo when tightening bolt is only run once
			for i in range(10):


				#if bolt threaded in and reaching bottom of travel command servo to open aperture
				if new_z <= 130 and open_servo_previously == False:
					servo_pos_msg.data = 20
					servo_pub.publish(servo_pos_msg.data)
					rospy.sleep(3)
					open_servo_previously = True

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


			#tighten bolt a couple more times without adjusting z axis
			stepperRun_pub.publish(800*2)
			#give time to unscrew bolt
			rospy.sleep(2)

			#move robot up and away from bolt
			robot.play(cmd = "lmove", rel = 0, z = 300, vel = 40, accel = 100,jerk = 1000, id = 300)
			robot.wait(id = 300, stat = 2)
			robot.play(cmd = "lmove", rel = 0, x = 300, vel = 40, accel = 100,jerk = 1000, id = 301)
			robot.wait(id = 301, stat = 2)


			#close connection to dorna robot, increase loop count
			robot.close()
			loop_counter = loop_counter + 1

		
		rate.sleep()



	rospy.loginfo("Robot disconnected and node stopped")
	
