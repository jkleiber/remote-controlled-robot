import cv2
import socket
import pickle
import struct ### new code

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('kleiber.xyz',6000))

while True:
    ret,frame = cap.read()
    data = pickle.dumps(frame) ### new code

    # Send message length first
    message_size = struct.pack("L", len(data))

    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code
