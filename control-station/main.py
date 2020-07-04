
import json
import socket
import threading
import time

from inputs import get_gamepad

from common.gamepad import LogitechF310Mapper

# Server info
server_addr = "10.0.0.3"
server_port = 5001
recv_port = 5003

# Set up UDP client for joystick data
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.setblocking(False)

recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind(('0.0.0.0', recv_port))
recv_sock.setblocking(False)

# Set up the gamepad processor
gamepad = LogitechF310Mapper()

# UDP loop update period
UDP_SEND_PERIOD = 0.05  # 10 ms -> 100Hz

# Relevant keys from gamepad
relevant_gamepad = ["ABS_Y", "ABS_RX"]

def init_gamepad():
    for key in relevant_gamepad:
        gamepad.set_relevant(key)

def monitor_gamepad():
    while True:
        # Get the latest gamepad events
        event_list = get_gamepad()

        # Process the gamepad events
        gamepad.update_relevant(event_list)

def udp_loop():
    # Send joystick input to server at a stable period.
    start_time = time.time()
    while True:
        # Get gamepad state and add timestamp
        gamepad_dict = gamepad.get_relevant_state()
        # TODO: add timestamp for packet watchdog

        # Send the gamepad state as a JSON string.
        control_pkt = (json.dumps(gamepad_dict) +"\r\n").encode()
        udp_sock.sendto(control_pkt, (server_addr, server_port))

        # Sleep until the period is up.
        while (time.time() - start_time) < UDP_SEND_PERIOD:
            continue

        # Set the start time for the next loop
        start_time = time.time()

        try:
            data = recv_sock.recvfrom(128)
        except Exception as e:
            continue
        else:
            print("Data: " + data.decode())


if __name__ == "__main__":
    # Create gamepad monitoring thread
    gamepad_thread = threading.Thread(target=monitor_gamepad)
    gamepad_thread.daemon = True
    gamepad_thread.start()

    # Initialize the gamepad
    init_gamepad()

    # Run main loop.
    udp_loop()