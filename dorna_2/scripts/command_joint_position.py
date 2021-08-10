#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState 

def callback_receive_JointStates(msg):
	rospy.loginfo(msg.position)
	


if __name__ == '__main__':
	rospy.init_node('command_joint_position')

	sub = rospy.Subscriber("/joint_states", JointState, callback_receive_JointStates) 
	
	rospy.spin()
