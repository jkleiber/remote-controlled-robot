#!/bin/bash

# Build the ROS2 workspace from within the docker image
cd /robot/ros2_ws && colcon build --symlink-install