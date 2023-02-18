import socket


# send function to Xclient
def send_to_xclient(message, server_address, buffer_size=1024):
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(str.encode(str({'message': message, 'addr': server_address})), xclient_address)
    msgFromServer = UDPClientSocket.recvfrom(buffer_size)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)


xclient_address = ("127.0.0.1", 20001)
