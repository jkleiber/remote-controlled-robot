#!/bin/bash

# Get config
source docker_config.sh

# Run the VPN.
sudo wg-quick up wg0

docker exec -it $CONTAINER_NAME bash -c "cd ros_workspace;. devel/setup.bash;roslaunch robot_launch robot.launch"

# Stop VPN
sudo wg-quick down wg0
