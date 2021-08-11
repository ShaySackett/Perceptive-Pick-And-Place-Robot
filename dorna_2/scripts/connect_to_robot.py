#!/usr/bin/env python3
import rospy
from dorna2 import dorna

def main():

    rospy.init_node('connect_to_robot')
    rospy.loginfo('Connect to robot node started')

    robot = dorna()

    ip = '10.33.6.1'
    port = 443
    robot.connect(ip, port)
    rospy.loginfo("Robot Connected!")

    while not rospy.is_shutdown():
        pass
    
    #close robot connection and websocket connection if robot is no longer connected
    else:
        robot.close()                              
        rospy.loginfo("Robot and websocket connection ended")



if __name__ == '__main__':
    main()
    
