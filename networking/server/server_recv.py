import socket

# Server info
host = '0.0.0.0'
port = 5001

# UDP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((host, port))

if __name__=="__main__":
    while True:
        try:
            print("waiting for data")
            data, addr = udp_sock.recvfrom(1024) # 1024 buffer size
            print(str(data.decode()) + ' from ' + str(addr))
        except Exception as e:
            print(str(e))
