#!/bin/bash

# Install WireGuard and dependencies
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:wireguard/wireguard
sudo apt install -y wireguard wireguard-dkms wireguard-tools

# Create Interface
sudo ip link add dev wg0 type wireguard

# Generate Keys
sudo wg genkey | sudo tee /etc/wireguard/privatekey | sudo wg pubkey | sudo tee /etc/wireguard/publickey
sudo chmod 600 /etc/wireguard/privatekey

# Reset interface (if needed).
sudo wg-quick down wg0
