# remote-controlled-robot

## What is this?
Software for controlling a robot over a VPN with a Logitech F310 Gamepad. The robot runs python on a raspberry pi, and is controlled with an arduino. A VPN connection is used to facilitate communication between a PC and the robot over the internet. Specifically, this project uses [WireGuard VPN](https://www.wireguard.com/) hosted on a private Vultr server.

## Video
[See the robot running here](https://kleiber.xyz/static/video/remote-control-demo.mp4)

## Setup Guide
### Requirements
- PC with Ubuntu 20.04*
- Raspberry Pi with Ubuntu Server 20.04*
- Docker installed on both the Raspberry Pi and PC  
- Logitech F310 Gamepad  
- [A robot with the required configuration](https://github.com/jkleiber/six-wheel-robot)
  
*This code probably works fine on other Ubuntu distributions, but has only been tested on Ubuntu 20.04

### Robot Setup
1. Ensure you can SSH into the Raspberry Pi
2. Install all the requirements
3. Ensure the robot has an internet connection. This involves messing with `wpa_supplicant`. You may need an ethernet cable at first to connect.  

### VPN Setup
1. [Follow the guide for setting up a VPN server here.](https://linuxize.com/post/how-to-set-up-wireguard-vpn-on-ubuntu-18-04/)  
  a. Ensure WireGuard is installed on the Raspberry Pi and your PC.  
  b. Configure your keys and add them to your server.  
  c. Ensure your PC's VPN IP will be 10.0.0.2 and your Raspberry Pi's VPN IP will be 10.0.0.3 (or change the code to your preference).  
  
## Running the System
1. SSH into the robot.  
2. Run `tmux` or your favorite terminal manager.  
3. Navigate to `robot/` and run `./start.sh`. This will launch the robot's docker container that runs all the code and manages dependencies.
4. Detach from your session (with `tmux`, this can be accomplished using Ctrl+B and then hitting the D key).  
  a. At this point, you can `exit` your SSH session if you want.  
5. Make sure the gamepad is plugged into your PC.  
6. On the PC, navigate to `control-station` and run `./start.sh`. This launches the control station docker container and sets up the joystick.  
7. The robot should be ready to run!  

## Stopping the System
1. Use Ctrl+C to stop the ground station contatiner.  
2. SSH into the robot.  
3. Reattach to the terminal session (for `tmux`, this would be a `tmux attach` or a `tmux attach -t #` where # is the session ID)
4. Use Ctrl+C to stop the robot process.  

## Testing
The `vpn-test` and `serial-test` folders contain docker containers that are run on the server and raspberry Pi respectively. `vpn-test` is used to ensure the PC and the VPN server have low latency, while `serial-test` is for checking the communication between the Raspberry Pi and the Arduino.
