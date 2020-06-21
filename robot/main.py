import cv2
import errno
import json
import numpy as np
import serial
import socket
import threading
import time

# Robot connection info, based on VPN setup.
control_ip = "10.0.0.2"
control_port = 5001
control_conn = (control_ip, control_port)
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

def video_process():
    while True:
        ret, frame = cap.read()

        # Only use valid frames.
        if ret:
            data = frame.flatten()
            data = data.tostring() #.encode()
        else:
            print('Invalid video frame')

def recv_control():
    while True:
        # Receive the control data.
        try:
            data, addr = ctrl_sock.recvfrom(256)
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                print("Receiver Error: " + str(e))
        else:
            # Make controls into meaningful robot messages.
            recv_dict = json.loads(data)
            turn = recv_dict['ABS_RX'] / 32768
            power = recv_dict['ABS_Y']

            # Form the robot input dictionary.
            ctrl_dict = {}
            ctrl_dict['power'] = power
            ctrl_dict['turn'] = turn

            # Convert to string
            ctrl_string = json.dumps(ctrl_dict)
            print(ctrl_string)

            # Publish to the robot.
            robot_usb.write(ctrl_string)

def heartbeat():
    while True:
        beat_str = "heartbeat".encode()

        try:
            heart_sock.sendto(beat_str, heart_conn)
        except Exception as e:
            print("Heartbeat Error: " + str(e))

        # Wait one second
        time.sleep(1)


if __name__=="__main__":
    # Initialize threads for the remote control receiver.
    ctrl_thread = threading.Thread(target=recv_control)
    video_thread = threading.Thread(target=video_process)
    heartbeat_thread = threading.Thread(target=heartbeat)

    # Start the threads
    ctrl_thread.start()
    video_thread.start()
    heartbeat_thread.start()
