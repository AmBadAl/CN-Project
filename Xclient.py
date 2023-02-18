import socket, threading


# Receive from client
def receive_from_client():
    # setting parameters
    local_IP = "127.0.0.1"
    local_port = 20001
    buffer_size = 1024
    # Create a datagram socket
    global UDPServerSocket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((local_IP, local_port))
    print("UDP server up and listening")
    # Listen for incoming datagrams
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(buffer_size)
        data = bytesAddressPair[0]
        address = bytesAddressPair[1]
        # convert data = {'message': message, 'server_addr': server_addr}
        # extract new address and message and send the result
        send_to_xserver(data['message'], data['server_addr'], address)


# Send to Xserver
def send_to_xserver(message, server_addr, client_addr):
    # send {message, client_address, server_addr} to xserver
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST_XSERVER, PORT_XSERVER))
        s.sendall(str({'message': message, 'server_addr': server_addr, 'client_addr': client_addr}).encode())


# receive from xserver
def receive_to_xserver():
    # receive {message, client_address, server_address} from xserver
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST_XCLIENT, PORT_XCLIENT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr} : receive_to_xserver")
            while True:
                # we assume data = {'message': message, 'client_addr': (client_host, client_port)}
                data = conn.recv(1024)
                print(data)
                data = dict(data)
                send_to_client(data['message'], data['client_addr'][0], data['client_addr'][1])
                # pass the message to the proper client


def send_to_client(message, server_address, client_address):
    UDPServerSocket.sendto(str.encode(str({'message': message, 'address': server_address})), client_address)


threading.Thread(target=receive_from_client).start()
threading.Thread(target=receive_to_xserver).start()

HOST_XSERVER = "127.0.0.1"
PORT_XSERVER = 65432
HOST_XCLIENT = "127.0.0.1"
PORT_XCLIENT = 21354
