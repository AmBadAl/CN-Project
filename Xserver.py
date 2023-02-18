import socket
import threading



# receive from xclient
def receive_from_xclient():
    # receive {message, client_address, server_address} from xclient
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST_XSERVER, PORT_XSERVER))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr} : receive_from_xclient")
            while True:
                # we assume data = {'message': message, 'client_addr': client_addr, 'server_addr': server_addr}
                data = conn.recv(1024)
                print(data)
                data = dict(data)
                send_to_server(message=data['message'], server_address=data['server_addr'], client_address=data['client_addr'])
                # pass the message to the proper server


# send to server
def send_to_server(message, server_address, client_address):
    UDPServerSocket.sendto(str.encode(str({'message': message, 'address': client_address})), server_address)


def receive_from_server():
    # setting parameters
    local_IP = "127.0.0.1"
    local_port = 8181
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
        # convert data = {'message': message, 'client_addr': client_addr}
        # extract new address and message and send the result
        send_to_xclient(message=data['message'], server_address=address, client_address=data['client_addr'])


# send to xclient
def send_to_xclient(message, server_address, client_address):
    # send {message, server_addr, client_address} to xclient
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST_XCLIENT, PORT_XCLIENT))
        s.sendall(str({'message': message, 'server_addr': server_address, 'client_addr': client_address}).encode())



HOST_XSERVER = "127.0.0.1"
PORT_XSERVER = 65432
HOST_XCLIENT = "127.0.0.1"
PORT_XCLIENT = 21354

threading.Thread(target=receive_from_xclient).start()
threading.Thread(target=receive_from_server).start()