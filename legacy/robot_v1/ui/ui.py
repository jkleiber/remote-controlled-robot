
import cv2
import json
import threading
import time

from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit

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

# Data
frame = None
jpg_buffer = None
frame_available = False
ctrl_status = {}

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

def update_frame(new_frame):
    global frame, frame_available
    # Collect the frame and note availability
    frame = new_frame
    frame_available = True

def update_control_input(ctrl_dict: dict):
    global ctrl_status
    ctrl_status = ctrl_dict

def new_error(err_str: str):
    global error_queue
    error_queue.append(err_str)