import socket
import struct
import sys

multicast_group = '224.0.0.251'
server_address = ('', 12345)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:

    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    print(f"Received {len(data)} bytes from {address}")

    print(data)

    print(f'sending acknowledgement to {address}')
    sock.sendto('ack'.encode(), address)
