#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from dorna2 import dorna 
import math

j_0 = JointState()
j_0_JSON = float()
old_j_0 = float()

def callback_receive_JointStates(msg):

	global j_0
	global j_0_JSON
	j_0 = msg.position[0]
	j_0_JSON = math.degrees(float(j_0)) #conver ROS radians to degrees for Dorna 2 API





if __name__ == '__main__':
	
	rospy.init_node('command_joint_position')

	robot = dorna()
	ip = '10.33.6.1'
	port = 443
	robot.connect(ip, port)
	rospy.loginfo("Robot Connected!")


	sub = rospy.Subscriber("/joint_states", JointState, callback_receive_JointStates) 
	


	while not rospy.is_shutdown():
		

		if old_j_0 != j_0_JSON:
			rospy.loginfo(str(j_0_JSON))
			robot.play(cmd = "jmove", rel = 0, j0 = j_0_JSON, vel = 10, accel = 100,jerk = 1000, id = 1)
			#robot.wait(id = 1, stat = 2)
			old_j_0 = j_0_JSON

	    
    #close robot connection and websocket connection if robot is no longer connected
	else:
		robot.close()                              
		rospy.loginfo("Robot and websocket connection ended")

	#rospy.spin()

	
	