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

### Robot serial ports.
robot_usb = None

### Set up videocapture.
cap = cv2.VideoCapture(0)
frame = None

### Game Controller
current_data = LogitechF310State()

# Skipped messages tracker
num_skipped = 0
SKIP_LIMIT = 5

def video_process():
    global frame
    while True:
        ret, frame = cap.read()
        UIServer.update_frame(frame)

def recv_control():
    global num_skipped

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

    # Convert to byte array for serial output.
    ctrl_string = (json.dumps(ctrl_dict) + "\n").encode()

    # Publish commands to the robot.
    try:
        robot_usb.write(ctrl_string)
    except:
        # If there is a serial error, just fail silently for now.
        pass
    else:
        # If the data was written successfully, show the output
        print(ctrl_string)

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

        time.sleep(LOOP_PERIOD)

        # Set the start time for the next loop
        start_time = time.time()


def initialize():
    try:
        robot_usb = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)#38400)
    except Exception as e:
        print(f"Serial Error: {e}. Serial may be unavailable")

if __name__=="__main__":
    # Initialize devices
    initialize()

    # Add time after start for the devices to initialize.
    time.sleep(1)

    # Main thread
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()

    # Video thread
    video_thread = threading.Thread(target=video_process)
    video_thread.start()

    # Flask Thread
    UIServer.start()
