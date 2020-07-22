import cv2
import errno
import json
import numpy as np
import serial
import socket
import threading
import time
import ui.ui as UIServer

from common.gamepad import LogitechF310State

# Loop control period
LOOP_PERIOD = 0.01

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

### Set up videocapture.
cap = cv2.VideoCapture(0)

### Game Controller
current_data = LogitechF310State()

# Skipped messages tracker
num_skipped = 0
SKIP_LIMIT = 5

def recv_control():
    global num_skipped, robot_usb

    # Attempt to receive the control data.
    try:
        data, addr = ctrl_sock.recvfrom(128)
    except socket.error as e:
        if e.errno != errno.EAGAIN:
            print("Receiver Error: " + str(e))
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
    turn = -1 * round(current_data.ABS_RX / 32768, 5)
    power = round(current_data.ABS_Y / 32768, 5)

    # Form the robot input dictionary.
    ctrl_dict = {}
    ctrl_dict['power'] = power
    ctrl_dict['turn'] = turn

    # Send control dictionary to server
    UIServer.update_control_input(ctrl_dict)

    # Convert to byte array for serial output.
    ctrl_string = (json.dumps(ctrl_dict) + "\n").encode()

    # Publish commands to the robot.
    try:
        robot_usb.write(ctrl_string)
    except Exception as e:
        # If there is a serial error, just fail silently for now.
        # print()
        serial_err = f'Serial FAIL: {e}'
        UIServer.new_error(serial_err)


def main():
    print('Hi from shamrock_teleop.')

    while True:
        # Get control data.
        recv_control()

        # Limit how fast the loop runs
        time.sleep(LOOP_PERIOD)


if __name__ == '__main__':
    main()
