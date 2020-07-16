FROM jkleiber8/opencv-python-embedded:base-4.3.0

WORKDIR /robot

EXPOSE 5001/udp
EXPOSE 5002/udp

# Install pipenv
RUN python3 -m pip install pipenv

# Run continuously
CMD tail -f /dev/null