FROM ros:noetic-perception-focal

WORKDIR /workspace

EXPOSE 5001/udp
EXPOSE 5002/udp

# Update repositories
RUN apt-get update

# Install pip
RUN apt-get install -y python3-pip

# Install pipenv
RUN python3 -m pip install pipenv

# Install dependencies from pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install pipenv packages globally
RUN pipenv lock --requirements > requirements.txt
RUN python3 -m pip install -r requirements.txt

CMD tail -f /dev/null
