#! /bin/bash
CONTAINER_NAME="robot-container"

# Ensure dependencies are installed
docker exec -i $CONTAINER_NAME ./install_robot_deps.sh

# Run the VPN.
sudo wg-quick up wg0

# Run the React Frontend


# Set up Ctrl+C trap
trap "./cleanup.sh" SIGINT

# Run the main robot program
docker exec -i $CONTAINER_NAME python -u main.py
