# VPN Setup

First, the WireGuard VPN must be installed on the server and the client(s) (Step 1 for each of the below steps). Once each Step 1 has been completed, you have enough information to complete the remaining steps of either setup path.

I recommend doing as much as possible using the config files rather than using the wireguard command line tools to set config, but that is my personal preference.

## Robot/PC Installation
1. Run `./install_vpn.sh` and follow the steps there.
2. Make a file named `wg0.conf` based on `example.conf` and fill out the public and private keys appropriate to your installation.
    a) You can find the public and private keys in `/etc/wireguard/(publickey, privatekey)`
    b) You can also find the public key by bringing the VPN up with `sudo wg-quick up wg0` and then showing the interface with `sudo wg show wg0`.
3. Run the `./config.sh` script to copy the config over to the wireguard configuration directory.

## Server Installation
1. Run `./install_vpn.sh` and follow the steps there.
2. Make a file named `wg0.conf` based on `example-server.conf` and fill out the public keys of the robot and the PC.
3. Run the `./config.sh` script to copy the config over to the wireguard configuration directory.

## Helpful Links
* [Wireguard Quick Start](https://www.wireguard.com/quickstart/)
* [Installation Guide](https://linuxize.com/post/how-to-set-up-wireguard-vpn-on-ubuntu-18-04/)
* [Solution to Common RTNETLINK Problem](https://stackoverflow.com/questions/37570910/rtnetlink-answers-operation-not-supported)