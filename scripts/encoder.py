#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry

def encoder_callback(msg):
    # Lay du lieu tu encoder (Odometry)
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    # Lay giu lieu van toc tu encoder
    linear_velocity = msg.twist.twist.linear.x
    angular_velocity = msg.twist.twist.angular.z

    # hien thi thong tin
    rospy.loginfo("Vị trí: x = {:.3f}, y = {:.3f}".format(x, y))
    rospy.loginfo("Vận tốc: Linear = {:.3f}, Angular = {:.3f}".format(linear_velocity, angular_velocity))

def encoder_listener():
    rospy.init_node('encoder_listener', anonymous=True)

    rospy.Subscriber("/odom", Odometry, encoder_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        encoder_listener()
    except rospy.ROSInterruptException:
        pass
