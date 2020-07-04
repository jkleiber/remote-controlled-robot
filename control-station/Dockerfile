FROM python:3.8.2

WORKDIR /teleop

# Install pipenv
RUN python3 -m pip install pipenv

# Install dependencies from pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv sync --dev

# Expose ports
EXPOSE 5001/udp
EXPOSE 5002/udp
EXPOSE 5003/udp

# Setup run command for control station
CMD ["pipenv", "run", "python3", "-u", "main.py"]
