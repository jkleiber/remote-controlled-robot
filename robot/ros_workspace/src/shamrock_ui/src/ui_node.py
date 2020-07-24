#!/usr/bin/python3

import cv2
import json
import rospy
import random
import threading
import time

from cv_bridge import CvBridge, CvBridgeError
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, PointCloud
from std_msgs.msg import String

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='{%',
        variable_end_string='%}',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

# App
app = CustomFlask(__name__, template_folder='./frontend', static_folder='./frontend/static')
app.config['SECRET_KEY'] = 'secret_password'
socketio = SocketIO(app)

# Vision
bridge = CvBridge()

# Data
frame = None
jpg_buffer = None
frame_available = False
ctrl_status = {
    'power': 0.0,
    'turn': 0.0
    }

origin = {"x": 0, "y": 0}
# LiDAR
obstacle_points = {
    "points": []
}

# Errors
error_queue = []

def data_stream():
    status = {}

    # Encode status
    status['time'] = time.time()
    for key, val in ctrl_status.items():
        status[f'control.{key}'] = val

    # Send status to the frontend
    socketio.emit('newData', status)

def lidar_data_stream():
    socketio.emit('lidar', obstacle_points)

def publish_errors():
    global error_queue

    error_pkt = {}
    num_errors = len(error_queue)
    for _ in range(num_errors):
        error_pkt['msg'] = error_queue.pop(0)
        socketio.emit('newError', error_pkt)

def camera_feed():
    global frame, frame_available
    while True:
        # Don't show frames if there hasn't been an update recently
        if frame_available is False:
            continue

        # Consume the frame
        frame_available = False

        # Encode into JPEG
        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 25])
        # jpg_buffer = cv2.imencode('.jpg', frame)[1]

        # Send data to frontend as well
        data_stream()
        lidar_data_stream()

        # Send errors to frontend
        publish_errors()

        # If JPEG encode is successful, show image
        if jpg_buffer is not None:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpg_buffer.tobytes() + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_stream')
def video_stream():
    return Response(camera_feed(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

def start(ip='0.0.0.0', port=5000):
    app.run(host=ip, port=port, threaded=True)

def update_frame(new_frame: Image):
    global frame, frame_available
    # Collect the frame and note availability
    frame = bridge.imgmsg_to_cv2(new_frame, 'passthrough')
    frame_available = True

def update_control_input(ctrl: Twist):
    global ctrl_status
    ctrl_status['power'] = ctrl.linear.x
    ctrl_status['turn'] = ctrl.angular.z

def update_lidar(point_cloud: PointCloud):
    global obstacle_points

    tmp_points = []

    # Update the obstacle points locally first
    for pt in point_cloud.points:
        tmp_points.append({
            "x": pt.x,
            "y": pt.y
        })

    obstacle_points['points'] = tmp_points

def new_error(error: String):
    global error_queue
    error_queue.append(error.data)

def ros_loop():
    rospy.init_node("ui_node")

    # Camera feed update
    image_sub = rospy.Subscriber("/camera_stream", Image, update_frame, queue_size=1)

    # Data feed updates
    control_input_sub = rospy.Subscriber("/control", Twist, update_control_input, queue_size=1)
    lidar_readings_sub = rospy.Subscriber("/point_cloud", PointCloud, update_lidar, queue_size=1)

    # Error feed updates
    error_sub = rospy.Subscriber("/error", String, new_error, queue_size=10)

    rospy.spin()

if __name__ == "__main__":
    # Flask Thread
    web_thread = threading.Thread(target = start, daemon = True).start()

    # ROS
    ros_loop()
