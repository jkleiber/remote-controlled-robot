FROM python:3.8.2

WORKDIR /ui

# Expose ports
EXPOSE 4200
EXPOSE 4201

# Copy SSL certs
COPY certs certs

# Install pipenv
RUN python3 -m pip install pipenv

# Install dependencies from pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install pipenv packages globally
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# Run uvicorn to start the video receiver app
CMD ["./ui_main.sh"]
# CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "4201", "--ssl-keyfile", "certs/kleiber.xyz.key", "--ssl-certfile", "certs/kleiber.xyz.crt"]