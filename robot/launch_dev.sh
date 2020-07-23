#!/bin/bash

# Get configuration
source docker_config.sh

docker exec -it $CONTAINER_NAME bash -c "cd ros_workspace;. devel/setup.bash;roslaunch shamrock_launch robot.launch"