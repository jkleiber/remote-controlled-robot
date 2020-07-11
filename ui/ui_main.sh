#!/bin/bash

# Start the image receiver in parallel
python -u img_recv_main.py &

# Start FastAPI server
uvicorn api_main:app --host 0.0.0.0 --port 4201 --ssl-keyfile certs/kleiber.xyz.key --ssl-certfile certs/kleiber.xyz.crt