#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

# Piano waypoint del percorso
waypoints = [
    [0, 0, 10],
    [10, 0, 15],
    [15, 10, 20]
]

def generate_path():
    path = Path()
    path.header.frame_id = "world"

    for wp in waypoints:
        pose = PoseStamped()
        pose.header.frame_id = "world"
        pose.pose.position.x = wp[0]
        pose.pose.position.y = wp[1] 
        pose.pose.position.z = wp[2]
        path.poses.append(pose)

    return path

if __name__ == "__main__":
    rospy.init_node("path_planner")

    path_pub = rospy.Publisher("/planned_path", Path, queue_size=10)
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        path_msg = generate_path()
        path_pub.publish(path_msg)
        
        rate.sleep()