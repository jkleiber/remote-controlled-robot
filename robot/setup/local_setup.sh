#!/bin/bash

###
# Local system dependency installation script
#
# NOTE: You don't need to run this if you are only planning on
#       using the docker images provided. This installs stuff at
#       the system level.
###

# One time installs
python3 -m pip install em
sudo apt install -y python3-catkin-pkg
python3 -m pip install pipenv

# Update with new python libraries
cp ../Pipfile ./
pipenv lock --requirements > requirements.txt
python3 -m pip install -r requirements.txt