FROM python:3.8.2

WORKDIR /app

EXPOSE 5001/udp
EXPOSE 5002/udp

# Install pipenv
RUN python3 -m pip install pipenv

# Install dependencies from pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install pipenv packages globally
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# Additional PC-only requirements
RUN pip install opencv-python

CMD ["python", "-u", "main.py"]
