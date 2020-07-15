
import cv2
import numpy as np
import threading

from flask import Flask, render_template, Response

cap = cv2.VideoCapture(0)
app = Flask(__name__)

frame = None

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    global frame
    while True:
        # Encode to JPG
        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        if ret_code:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpg_buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def video_capturer():
    global frame
    while True:
        ret, frame = cap.read()


if __name__ == '__main__':
    video_thread = threading.Thread(target = video_capturer)
    video_thread.start()

    app.run(host='0.0.0.0', threaded=True)