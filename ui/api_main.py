
import io
import time

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse

app = FastAPI()

latest_img = None

# def video_stream():
#     # while True:
#     # Load the latest image
#     latest_img = open("latest.jpg", "rb")
#     latest_img = io.BytesIO(latest_img.tobytes())
#     yield latest_img


# @app.get("/stream")
# def video_stream_main():
#     # latest_img = open("latest.jpg", "rb")
#     return StreamingResponse(video_stream(), media_type="image/jpg")

@app.get("/stream")
async def img_stream():
    return FileResponse("latest.jpg")

@app.get("/")
def main():
    return FileResponse("static/index.html")
