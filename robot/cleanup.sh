#! /bin/bash
CONTAINER_NAME="robot-container"

# Kill the running program
docker exec robot-container kill $(docker exec robot-container pgrep python)

# Stop the VPN.
sudo wg-quick down wg0
