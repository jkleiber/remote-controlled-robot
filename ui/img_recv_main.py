
import cv2
import imagezmq

# ImageZMQ images
image_hub = imagezmq.ImageHub(open_port='tcp://0.0.0.0:4200')

# Store latest image
latest_img = None

def video_recv():
    # print("waiting")
    # Receive a JPG image from ImageZMQ
    _, latest_img = image_hub.recv_jpg()
    # print('received')

    # Acknowledge receipt
    image_hub.send_reply(b'OK')

    # Save image
    with open("latest.jpg", "wb") as f:
        f.write(latest_img)

if __name__=="__main__":
    while True:
        video_recv()