import cv2
import numpy as np
import socket

# Host info
host = "kleiber.xyz"
port = 5001

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1) # 1 sec timeout

# Set up videocapture
cap = cv2.VideoCapture(0)

if __name__=="__main__":
    while True:
        ret, frame = cap.read()

        # Only use valid frames
        if ret:
            # Stringify data
            data = frame.flatten()
            data = data.tostring()
            data = "hello server" # Hack to check if this works
            # Send over socket
            try:
                sock.sendto(data.encode(), (host, port))
            except Exception as e:
                print('Error with UDP stream: ' + str(e))
        else:
            print('Invalid video frame')

