import socket
import struct
import sys

multicast_group4 = '224.3.29.71'
multicast_group6 ='ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
group_cast = multicast_group6
server_address = ('', 10000)

# Create the socket
# Initialise socket for IPv6 datagrams
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allows address to be reused
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Binds to all interfaces on the given port
sock.bind(('', 8080))

# Allow messages from this socket to loop back for development
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)

# Construct message for joining multicast group
mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

data, addr = sock.recvfrom(1024)
print(data)
# Create ipv6 datagram socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
# Allow own messages to be sent back (for local testing)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
sock.sendto("hello world".encode('utf-8'), ("ff02::abcd:1", 8080))
