#!/usr/bin/python3

import cv2
import rospy

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

### Set up videocapture.
cap = cv2.VideoCapture(0)

### Image publisher
image_pub = rospy.Publisher("/camera_stream", Image, queue_size=1)

### Error publisher
error_pub = rospy.Publisher('/error', String, queue_size=1)

### OpenCV Bridge
bridge = CvBridge()

def make_480p():
    change_res(640, 480)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

def video_feed(time):
    # Read an image from the camera
    ret, frame = cap.read()

    # If we got an image, try to send it to the GUI
    if ret:
        try:
            ros_frame = bridge.cv2_to_imgmsg(frame, 'passthrough')
        except CvBridgeError as err:
            err_str = String(data = str(err))
            error_pub.publish(err_str)
        else:
            image_pub.publish(ros_frame)

def main():
    rospy.init_node("vision_node")

    make_480p()

    video_timer = rospy.Timer(rospy.Duration(0.01), video_feed)

    rospy.spin()

if __name__ == "__main__":
    main()