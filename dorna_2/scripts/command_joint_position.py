#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from dorna2 import dorna 
import math

#initialize array that stores angular position of robotic arm using JointState data type. 
ros_position = JointState()
old_position = JointState()

#initialize variables that will store angular values of robot joints as regular floats then command robot within the Dorna API
#Added a 'JSON' suffix to differentiate this variable from "j0,j1" etc keys in robot.play command
j_0_JSON = float()
j_1_JSON = float()

def callback_receive_JointStates(msg):

	#bring global variables into local scope
	global ros_position
	global j_0_JSON
	global j_1_JSON
	
	#update position of robot arm from JointState message type
	ros_position = msg.position
	

	#pull each joints' respective angular position from ros_position array, then convert JointState type to a float, then convert from radians in ROS to degrees for Dorna 2 API,
	j_0_JSON = math.degrees(float(ros_position[0]))
	j_1_JSON = math.degrees(float(ros_position[1])) #need to add pi here since ROS and Dorna Coordinate "zeroes" are offset from one another





if __name__ == '__main__':
	
	rospy.init_node('command_joint_position')

	robot = dorna()
	ip = '10.33.6.1'
	port = 443
	robot.connect(ip, port)
	rospy.loginfo("Robot Connected!")


	sub = rospy.Subscriber("/joint_states", JointState, callback_receive_JointStates) 
	
	id_counter = 0

	while not rospy.is_shutdown():

		
		if (old_position != ros_position):
			
			rospy.loginfo(str(math.radians(j_0_JSON)) + " , " +str(math.radians(j_1_JSON)))
			robot.play(cmd = "jmove", rel = 0, j0 = j_0_JSON, j1 = j_1_JSON, vel = 10, accel = 100,jerk = 1000, id = id_counter)
			#robot.wait(id = id_counter, stat = 2)

			id_counter += 1
			old_position = ros_position
			
			

	    
    #close robot connection and websocket connection if robot is no longer connected
	else:
		robot.close()                              
		rospy.loginfo("Robot and websocket connection ended")

	#rospy.spin()

	
	