import socket
import struct
import sys

message = 'very important data'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
# Create ipv6 datagram socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
# Allow own messages to be sent back (for local testing)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
sock.sendto("hello world".encode('utf-8'), ("ff02::abcd:1", 8080))
