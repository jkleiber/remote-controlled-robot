import sys
import time
import numpy as np
import cv2
import imagezmq
import socket

# Video capture
cap = cv2.VideoCapture(0)

# sender = imagezmq.ImageSender(connect_to='tcp://kleiber.xyz:4200')

local_host = socket.gethostname()
jpeg_quality = 90

while True:  # press Ctrl-C to stop image sending program
    # Capture video frame
    ret, frame = cap.read()
    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Encode to JPG
    # ret_code, jpg_buffer = cv2.imencode(
    #     ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

    # Send JPG
    # try:
    #     sender.send_jpg(local_host, jpg_buffer)
    # except Exception as e:
    #     print(f"ZMQ send failed! {e}")
    sys.stdout.write( str(frame.tobytes()) )

cv2.destroyAllWindows()
