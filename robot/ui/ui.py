
import cv2

from flask import Flask, render_template, Response

app = Flask(__name__)
frame = None

def camera_feed():
    global frame
    while True:
        # Encode to JPG
        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        if ret_code:
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
    global frame
    frame = new_frame
