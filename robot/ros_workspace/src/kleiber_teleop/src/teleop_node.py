#!/usr/bin/python3

import cv2
import errno
import json
import numpy as np
import rospy
import serial
import socket
import time

from gamepad import LogitechF310State
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# Control station connection info, based on VPN setup.
robot_ip = "0.0.0.0"
control_ip = "10.0.0.2"
control_port = 5001
control_conn = (robot_ip, control_port)

### Set up UDP sockets.
# Control.
ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ctrl_sock.bind(control_conn)
ctrl_sock.setblocking(False)

### Robot serial ports.
robot_usb = None

### Game Controller
current_data = LogitechF310State()

# Skipped messages tracker
num_skipped = 0
SKIP_LIMIT = 5

### Publishers
error_pub = rospy.Publisher('/error', String, queue_size=1)
ctrl_pub = rospy.Publisher('/control', Twist, queue_size=1)

def recv_control(time):
    global num_skipped, robot_usb

    # Make new twist object
    control = Twist()

    # Attempt to receive the control data.
    try:
        data, addr = ctrl_sock.recvfrom(128)
    except socket.error as e:
        if e.errno != errno.EAGAIN:
            err = String(data = "Receiver Error: " + str(e))
            error_pub.publish(err)
        num_skipped += 1
    else:
        # Make controls into meaningful robot messages.
        recv_dict = json.loads(data)

        # Update data.
        current_data.ABS_RX = recv_dict['ABS_RX']
        current_data.ABS_Y = recv_dict['ABS_Y']

        # Reset skipped message tracker.
        num_skipped = 0

    # If we have skipped too many messages, stop the robot.
    if num_skipped > SKIP_LIMIT:
        current_data.ABS_RX = 0
        current_data.ABS_Y = 0

    # Find the appropriate control from the given packet.
    control.angular.z = -0.75 * round(current_data.ABS_RX / 32768, 5)
    control.linear.x = 0.75 * round(current_data.ABS_Y / 32768, 5)

    # Form the robot input dictionary.
    ctrl_dict = {}
    ctrl_dict['power'] = control.linear.x
    ctrl_dict['turn'] = control.angular.z

    # Send control dictionary to server
    ctrl_pub.publish(control)

    # Convert to byte array for serial output.
    ctrl_string = (json.dumps(ctrl_dict) + "\n").encode()

    # Publish commands to the robot.
    try:
        robot_usb.write(ctrl_string)
    except Exception as e:
        serial_err = f'Serial FAIL: {e}'
        err_str = String(data = serial_err)
        error_pub.publish(err_str)

def main_loop():
    # Initialize node
    rospy.init_node("teleop_node")

    # Get control data at a specific rate.
    recv_timer = rospy.Timer(rospy.Duration(0.025), recv_control)

    # Spin
    rospy.spin()


def initialize():
    global robot_usb

    try:
        robot_usb = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
    except Exception as e:
        print(f"Serial Error: {e}. Serial may be unavailable")

if __name__=="__main__":
    # Initialize devices
    initialize()

    # Add time after start for the devices to initialize.
    time.sleep(1)

    # Main program loop
    main_loop()
