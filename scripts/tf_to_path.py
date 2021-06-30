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
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import PoseStamped

import sys
import signal

def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


''' class '''

class path_pub():
    def __init__(self):
        rospy.init_node('path_pubb', anonymous=True)
        self.parent_frame_id = rospy.get_param("~parent_frame_id", '/world')
        self.child_frame_id = rospy.get_param("~child_frame_id", '/imu')
        self.out_topic_name = rospy.get_param("~out_topic_name", '/my_path')
        self.append_rate = rospy.get_param("~append_rate", 25)
        self.my_pose = rospy.Subscriber('/tf', TFMessage, self.tfcallback)
        self.my_path_pub = rospy.Publisher(self.out_topic_name, Path, queue_size=1)


        self.rate = rospy.Rate(self.append_rate)
        self.my_path = Path()
        self.check = 0

    def tfcallback(self, msg):
        for i in range(len(msg.transforms)):
            if msg.transforms[i].header.frame_id==self.parent_frame_id and msg.transforms[i].child_frame_id==self.child_frame_id:
                self.pose = msg.transforms[i].transform
                self.check = 1

''' main '''
path_pub_class = path_pub()

if __name__ == '__main__':
    while 1:
        try:
            if path_pub_class.check == 1:
                pose = PoseStamped()
                pose.pose.position.x = path_pub_class.pose.translation.x
                pose.pose.position.y = path_pub_class.pose.translation.y
                pose.pose.position.z = path_pub_class.pose.translation.z
                pose.pose.orientation.x = path_pub_class.pose.rotation.x
                pose.pose.orientation.y = path_pub_class.pose.rotation.y
                pose.pose.orientation.z = path_pub_class.pose.rotation.z
                pose.pose.orientation.w = path_pub_class.pose.rotation.w
                pose.header.frame_id = path_pub_class.parent_frame_id
                pose.header.stamp = rospy.Time.now()
                path_pub_class.my_path.header.frame_id=path_pub_class.parent_frame_id
                path_pub_class.my_path.poses.append(pose)
                path_pub_class.my_path.header.stamp = rospy.Time.now()
                path_pub_class.my_path_pub.publish(path_pub_class.my_path)

                path_pub_class.rate.sleep()
        except (rospy.ROSInterruptException, SystemExit, KeyboardInterrupt) :
            sys.exit(0)
        # except:
        #     print("exception")
        #     pass
