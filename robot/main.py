import cv2
import errno
import json
import numpy as np
import serial
import socket
import threading
import time

from common.gamepad import LogitechF310State

# Loop control period
LOOP_PERIOD = 0.02

# Control station connection info, based on VPN setup.
robot_ip = "0.0.0.0"
control_ip = "10.0.0.2"
control_port = 5001
control_conn = (robot_ip, control_port)
heart_port = 5002
heart_conn = (control_ip, heart_port)

### Set up UDP sockets.
# Control.
ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ctrl_sock.bind(control_conn)
ctrl_sock.setblocking(False)

# Heartbeat
heart_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
heart_sock.setblocking(True)

# Video.
video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_sock.settimeout(1) # 1 sec timeout.

### Robot serial ports.
robot_usb = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

### Set up videocapture.
cap = cv2.VideoCapture(0)

### Game Controller
default_pkt = LogitechF310State()

def video_process():
    ret, frame = cap.read()

    # Only use valid frames.
    if ret:
        data = frame.flatten()
        data = data.tostring() #.encode()
    else:
        print('Invalid video frame')

def recv_control():
    # Set the receive to the default.
    recv_dict = vars(default_pkt)

    # Attempt to receive the control data.
    try:
        data, addr = ctrl_sock.recvfrom(128)
    except socket.error as e:
        if e.errno != errno.EAGAIN:
            print("Receiver Error: " + str(e))
    else:
        # Make controls into meaningful robot messages.
        recv_dict = json.loads(data)

    # Find the appropriate control from the given packet.
    turn = int(recv_dict['ABS_RX']) / 32768
    power = int(recv_dict['ABS_Y']) / 32768

    # Form the robot input dictionary.
    ctrl_dict = {}
    ctrl_dict['power'] = power
    ctrl_dict['turn'] = turn

    # Convert to byte array for serial output.
    ctrl_string = json.dumps(ctrl_dict).encode()
    print(ctrl_string)

    print(robot_usb.out_waiting)
    # Publish to the robot.
    robot_usb.write(ctrl_string)
    data = robot_usb.read_until()
    print(f'Response: {data}')

def heartbeat():
    beat_str = "heartbeat".encode()
    try:
        heart_sock.sendto(beat_str, heart_conn)
    except Exception as e:
        print("Heartbeat Error: " + str(e))

def main_loop():
    # Limit the loop rate for control
    # TODO: do something better than this (i.e. multiprocess)
    start_time = 0
    while True:
        # Get control data.
        recv_control()

        # Get video.
        # video_process()

        # Send heartbeat back to control station.
        # heartbeat()

        # Slow down the loop
        # Sleep until the period is up.
        # while (time.time() - start_time) < LOOP_PERIOD:
            # continue

        time.sleep(0.02)

        # Set the start time for the next loop
        start_time = time.time()


if __name__=="__main__":
    # Add time after start for the devices to initialize.
    time.sleep(1)

    # Start looping.
    main_loop()
