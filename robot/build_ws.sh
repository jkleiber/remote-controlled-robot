#!/bin/bash

source docker_config.sh

docker exec -it $CONTAINER_NAME bash -c "cd ros_workspace;rm -rf build;. devel/setup.bash;catkin_make;. devel/setup.bash"