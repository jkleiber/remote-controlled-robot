
import json
import socket
import threading

from common.gamepad import LogitechF310State

# Server and robot info.
host = '0.0.0.0'
robot_ip = None

# Ports.
ctrl_recv_port = 5001
robot_send_port = 5002
robot_heart_port = 5003

# Connections.
ctrl_recv_conn = (host, ctrl_recv_port)
robot_conn = (robot_ip, robot_send_port)
heart_conn = (host, robot_heart_port)

### UDP sockets.
# Receive control from groundstation.
ctrl_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ctrl_recv_sock.bind(ctrl_recv_conn)
ctrl_recv_sock.setblocking(False)

# Send packets to robot.
robot_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
robot_send_sock.setblocking(False)

# Receive robot heartbeat.
heart_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
heart_sock.bind(heart_conn)
heart_sock.setblocking(True)

default_pkt = LogitechF310State()

def control_passthrough():
    while True:
        # Set the control to the default packet.
        ctrl_pkt = vars(default_pkt)

        # Process data in non-blocking fashion.
        try:
            data, addr = ctrl_recv_sock.recvfrom(256)
            print(str(data.decode()) + ' from ' + str(addr))
        except socket.timeout as e:
            pass
        except Exception as e:
            print("Control Receive Error: " + str(e))
        # If everything went well, establish the control data as the packet.
        else:
            ctrl_pkt = data

        # Process the control packet.
        ctrl_str = json.dumps(ctrl_pkt).encode()

        # Send data to the robot if we know the robot's IP address.
        if robot_ip is not None:
            try:
                robot_send_sock.sendto(ctrl_str, robot_conn)
            except Exception as e:
                print("Control Send Error: " + str(e))

def robot_heartbeat():
    while True:
        try:
            # TODO: add more advanced password via data.
            data, addr = heart_sock.recvfrom(64)

            # Set robot IP
            if data.decode() == 'heartbeat':
                robot_ip = addr
                robot_conn = (robot_ip, robot_send_port)
        except Exception as e:
            print("Heartbeat Error: " + str(e))

if __name__=="__main__":
    # Set up threads.
    ctrl_thread = threading.Thread(target=control_passthrough)
    heart_thread = threading.Thread(target=robot_heartbeat)

    # Start threads.
    ctrl_thread.start()
    heart_thread.start()
