FROM python:3.8.2

WORKDIR /app

EXPOSE 5001/udp
EXPOSE 5002/udp

# Install pipenv
RUN python3 -m pip install pipenv

# Run continuously
CMD tail -f /dev/null
