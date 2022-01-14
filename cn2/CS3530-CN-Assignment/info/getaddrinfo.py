#! /usr/bin/env python3
import socket
import sys
import os

if len(sys.argv)!=3:
	print("<usage>: <run> <hostname> <port>")
	exit()
host = sys.argv[1]
port = sys.argv[2]										#to capture the tcp dump and use get addr info correspondigly
addrinfo = socket.getaddrinfo(host,port)
#addrs = socket.getaddrinfo("localhost", port, socket.AF_INET6, 0, socket.SOL_TCP)
print(addrinfo)
#print(addrs)