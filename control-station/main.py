
import json
import socket
import threading
import time

from inputs import get_gamepad

from gamepad import LogitechF310Mapper

# Server info
server_addr = "kleiber.xyz"
server_port = 5001

# Set up UDP client for joystick data
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.setblocking(False)

# Set up the gamepad processor
gamepad = LogitechF310Mapper()

# UDP loop update period
UDP_SEND_PERIOD = 0.02  # 10 ms -> 100Hz

def monitor_gamepad():
    while True:
        # Get the latest gamepad events
        event_list = get_gamepad()

        # Process the gamepad events
        gamepad.update(event_list)

def udp_loop():
    # Send joystick input to server at a stable period.
    start_time = time.time()
    while True:
        # Get gamepad state and add timestamp
        gamepad_dict = gamepad.get_state()
        gamepad_dict['timestamp'] =

        # Send the gamepad state as a JSON string.
        control_pkt = json.dumps(gamepad_dict).encode()
        udp_sock.sendto(control_pkt, (server_addr, server_port))

        # Sleep until the period is up.
        while (time.time() - start_time) < UDP_SEND_PERIOD:
            continue

        # Set the start time for the next loop
        start_time = time.time()


if __name__ == "__main__":
    # Create gamepad monitoring thread
    gamepad_thread = threading.Thread(target=monitor_gamepad)
    gamepad_thread.daemon = True
    gamepad_thread.start()

    # Run main loop.
    udp_loop()