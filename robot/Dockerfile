FROM jkleiber8/opencv-python-embedded:base-4.3.0

WORKDIR /app

EXPOSE 5001/udp

RUN python -m pip install pyserial

CMD ["python", "-u", "main.py"]
