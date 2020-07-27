#!/bin/bash

cd "$(dirname "$0")"

# Add user to dialout
sudo adduser $USER dialout

# Update udev rules
sudo cp ./robot.rules /etc/udev/rules.d/robot.rules

# Restart udev
sudo service udev reload
sleep 2
sudo service udev restart
sudo udevadm trigger
