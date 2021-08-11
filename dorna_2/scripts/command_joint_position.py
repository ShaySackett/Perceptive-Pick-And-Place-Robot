#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from dorna2 import dorna 



def callback_receive_JointStates(msg):

	
	j_0 = msg.position[0]
	j_1 = msg.position[1]
	j_2 = msg.position[2]
	j_3 = msg.position[3]
	j_4 = msg.position[4]

	

	
def main():
	rospy.init_node('command_joint_position')

	robot = dorna()
	ip = '10.33.6.1'
	port = 443
	robot.connect(ip, port)
	rospy.loginfo("Robot Connected!")


	sub = rospy.Subscriber("/joint_states", JointState, callback_receive_JointStates) 
	

	robot.play(cmd = "jmove", rel = 0, j0 = 0, vel = 10, accel = 100,jerk = 1000, id = 1)
	robot.wait(id = 1, stat = 2)



	while not rospy.is_shutdown():
		pass
    
    #close robot connection and websocket connection if robot is no longer connected
	else:
		robot.close()                              
		rospy.loginfo("Robot and websocket connection ended")

	rospy.spin()
	


	


if __name__ == '__main__':
	main()

	
	