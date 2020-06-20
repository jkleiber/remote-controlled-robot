
import socket

from inputs import get_gamepad

# Server info
server_addr = "kleiber.xyz"
server_port = 5001

# Set up UDP client for joystick data
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def loop():
    # Send joystick input to server continuously.
    while True:
        # Get the latest gamepad events
        events = get_gamepad()

        # Go through each event and send a message to the server
        for event in events:
            event_str = str(event.ev_type) + ": " + str(event.code) + " - " + str(event.state)
            udp_sock.sendto(event_str.encode(), (server_addr, server_port))


if __name__ == "__main__":
    # Run main loop.
    loop()