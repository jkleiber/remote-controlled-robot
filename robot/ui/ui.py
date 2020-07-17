
import cv2
import time

from flask import Flask, render_template, Response

app = Flask(__name__)

frame = None
jpg_buffer = None
frame_available = False

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
