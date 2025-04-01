#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import sys, termios, tty

LINEAR_SPEED = 0.2
ANGULAR_SPEED = 1

ARM_STEP = 0.1

NAMESPACE = ""

KEY_MAPPING = {
    'w': ('wheel', [LINEAR_SPEED, 0.0]),    # tien
    's': ('wheel', [-LINEAR_SPEED, 0.0]),   # lui
    'a': ('wheel', [0.0, ANGULAR_SPEED]),   # Quay trai
    'd': ('wheel', [0.0, -ANGULAR_SPEED]),  # Quay phai
    'i': ('arm1', ARM_STEP),                # Tang arm1
    'k': ('arm1', -ARM_STEP),               # Giam arm1
    'j': ('arm2', ARM_STEP),                # Tang arm2
    'l': ('arm2', -ARM_STEP),               # Giam arm2
    'q': ('exit', None)                     # out
}

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def teleop_control():
    rospy.init_node("teleop_robot", anonymous=True)

    # Publisher
    wheel_pub = rospy.Publisher(f"{NAMESPACE}/cmd_vel", Twist, queue_size=10)
    arm1_pub = rospy.Publisher(f"{NAMESPACE}/arm_1_joint_controller/command", Float64, queue_size=10)
    arm2_pub = rospy.Publisher(f"{NAMESPACE}/arm_2_joint_controller/command", Float64, queue_size=10)

    rate = rospy.Rate(10)
    rospy.sleep(1) 

    if wheel_pub.get_num_connections() == 0:
        rospy.logwarn("Khong co subscriber nao ket noi toi /cmd_vel!")
    else:
        rospy.loginfo("da ket noi toi /cmd_vel")
    if arm1_pub.get_num_connections() == 0:
        rospy.logwarn("khong co subscriber nao ket noi toi /arm_1_joint_controller/command!")
    else:
        rospy.loginfo("da ket noi toi /arm_1_joint_controller/command")
    if arm2_pub.get_num_connections() == 0:
        rospy.logwarn("khong co subscriber nao ket noi toi /arm_2_joint_controller/command!")
    else:
        rospy.loginfo("da ket noi toi /arm_2_joint_controller/command")

    rospy.loginfo("=== TELEOP CONTROL ===")
    rospy.loginfo("W - Tien | S - Lui | A - Quay trai | D - Quay phai")
    rospy.loginfo("I - Tang arm1 | K - Giam arm1 | J - Tang arm2 | L - Giam arm2")
    rospy.loginfo("Q - out")

    twist = Twist()
    arm1_pos = 0.0
    arm2_pos = 0.0

    while not rospy.is_shutdown():
        key = get_key()

        if key in KEY_MAPPING:
            action_type, value = KEY_MAPPING[key]

            if action_type == 'exit':
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                wheel_pub.publish(twist)
                rospy.loginfo("Thoát chương trình!")
                break

            elif action_type == 'wheel':
                twist.linear.x = value[0]
                twist.angular.z = value[1]
                wheel_pub.publish(twist)
                rospy.loginfo(f"Wheel - Linear: {twist.linear.x}, Angular: {twist.angular.z}")

            elif action_type == 'arm1':
                arm1_pos += value
                arm1_pos = max(-1.57, min(1.57, arm1_pos))
                arm1_pub.publish(Float64(arm1_pos))
                rospy.loginfo(f"Arm1 position: {arm1_pos:.2f} rad")

            elif action_type == 'arm2':
                arm2_pos += value
                arm2_pos = max(-1.57, min(1.57, arm2_pos))
                arm2_pub.publish(Float64(arm2_pos))
                rospy.loginfo(f"Arm2 position: {arm2_pos:.2f} rad")

        elif key == '\x03':  # Ctrl+C
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            wheel_pub.publish(twist)
            rospy.loginfo("Thoát bằng Ctrl+C!")
            break

        rate.sleep()

if __name__ == "__main__":
    try:
        teleop_control()
    except rospy.ROSInterruptException:
        rospy.loginfo("da dung boi ROS Interrupt")
    except Exception as e:
        rospy.logerr(f"Loi xay ra: {str(e)}")