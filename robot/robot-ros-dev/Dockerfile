FROM osrf/ros:foxy-desktop

WORKDIR /robot

# Update package list
RUN apt-get update && apt-get upgrade -y

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

# Additional PC-only requirements
RUN python3 -m pip install opencv-python

# Keep alive in detached mode
CMD tail -f /dev/null