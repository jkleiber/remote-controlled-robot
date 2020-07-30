#!/bin/bash

#
# Edit example.conf and rename it to wg0.conf before configuring the VPN.
# This works for the server example too.
#

# Copy the local config to the wireguard configuration
sudo cp wg0.conf /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf