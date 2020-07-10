FROM python:3.8.2

WORKDIR /app

RUN python -m pip install opencv-python

EXPOSE 6000/udp

CMD ["python", "-u", "server_cv.py"]