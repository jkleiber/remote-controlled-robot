#! /bin/bash

# Install pipenv packages globally
pipenv lock --requirements > requirements.txt
pip install -r requirements.txt