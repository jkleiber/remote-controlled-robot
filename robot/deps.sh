#!/bin/bash

# One time installs
# python3 -m pip install em
# sudo apt install -y python3-catkin-pkg
python3 -m pip install pipenv

# Update with new python libraries
pipenv lock --requirements > requirements.txt
python3 -m pip install -r requirements.txt