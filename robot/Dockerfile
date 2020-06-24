FROM jkleiber8/opencv-python-embedded:base-4.3.0

WORKDIR /app

RUN python -m pip install pyserial

EXPOSE 5001/udp
EXPOSE 5002/udp

CMD ["python", "-u", "main.py"]
