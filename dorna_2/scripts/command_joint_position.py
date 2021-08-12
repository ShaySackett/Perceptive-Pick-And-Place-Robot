#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from dorna2 import dorna 

j_0 = JointState()
new_j_0 = float()

def callback_receive_JointStates(msg):

	global j_0
	global new_j_0
	j_0 = msg.position[0]
	new_j_0 = float(j_0)


if __name__ == '__main__':
	
	rospy.init_node('command_joint_position')

	robot = dorna()
	ip = '10.33.6.1'
	port = 443
	robot.connect(ip, port)
	rospy.loginfo("Robot Connected!")


	sub = rospy.Subscriber("/joint_states", JointState, callback_receive_JointStates) 
	

	robot.play(cmd = "jmove", rel = 0, j0 = new_j_0, vel = 10, accel = 100,jerk = 1000, id = 1)
	robot.wait(id = 1, stat = 2)



	while not rospy.is_shutdown():
		pass
    
    #close robot connection and websocket connection if robot is no longer connected
	else:
		robot.close()                              
		rospy.loginfo("Robot and websocket connection ended")

	rospy.spin()

	
	