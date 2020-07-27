#!/bin/bash

source docker_config.sh

docker exec -it $CONTAINER_NAME bash -c "cd ros_workspace;rm -rf build;source /opt/ros/noetic/setup.bash;catkin_make -j1;. devel/setup.bash"
