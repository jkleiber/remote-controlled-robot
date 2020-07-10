FROM python:3.8.2

WORKDIR /app

RUN python -m pip install pyserial opencv-python

EXPOSE 5001/udp
EXPOSE 5002/udp

CMD ["python", "-u", "main.py"]
