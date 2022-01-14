#!/usr/bin/env python3
import socket
import sys
import os
									#socket creation
if len(sys.argv)!=3:
	print("<usage>:<run> <host> <port>")
	exit()
addrinfo = socket.getaddrinfo(sys.argv[1], None)[0]
sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)

sock.connect((sys.argv[1],int(sys.argv[2])))
print("Connection Established")
						# send this to the server and get it back
print("Type: ",end='')				#taking input from the user
s = input()
sock.send(s.encode())
ans = sock.recv(1024)
print("Received: "+ans.decode())
print("Connection closed")
sock.close()