#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 00:28:30 2020

@author: mason
"""

''' import libraries '''
import time
import numpy as np

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from gazebo_msgs.msg import ModelStates

import sys
import signal

def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


''' class '''

class path_pub():
    def __init__(self):
        rospy.init_node('gt_path_pubb', anonymous=True)
        self.parent_frame_id = rospy.get_param("~parent_frame_id", 'world')
        self.append_rate = rospy.get_param("~append_rate", 25)
        self.robot_name = rospy.get_namespace()

        self.gt_path_pub = rospy.Publisher("gt_path", Path, queue_size=2)
        self.gt_poses = rospy.Subscriber("/gazebo/model_states", ModelStates, self.gtcallback)


        self.my_path = Path()
        self.check = 0

        self.rate = rospy.Rate(self.append_rate)

    def gtcallback(self, msg):
        for i in range(len(msg.name)):
            if msg.name[i]==self.robot_name[1:-1]:
                self.pose = msg.pose[i]
                self.check= 1

''' main '''
path_pub_class = path_pub()

if __name__ == '__main__':
    while 1:
        try:
            if path_pub_class.check == 1:
                pose = PoseStamped()
                pose.pose = path_pub_class.pose
                pose.header.frame_id = path_pub_class.parent_frame_id
                pose.header.stamp = rospy.Time.now()
                path_pub_class.my_path.poses.append(pose)
                path_pub_class.my_path.header.frame_id = path_pub_class.parent_frame_id 
                path_pub_class.my_path.header.stamp = rospy.Time.now()
                path_pub_class.gt_path_pub.publish(path_pub_class.my_path)
            path_pub_class.rate.sleep()
        except (rospy.ROSInterruptException, SystemExit, KeyboardInterrupt) :
            sys.exit(0)
        # except:
        #     print("exception")
        #     pass
