#!/bin/bash

# Get configuration
source docker_config.sh

LAUNCH_ARGS="$@"

docker exec -it $CONTAINER_NAME bash -c "cd ros_workspace;. devel/setup.bash;roslaunch ${LAUNCH_ARGS}"