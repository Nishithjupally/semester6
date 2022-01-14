#!/usr/bin/env python3
import socket
import os
import sys
import threading



if len(sys.argv)!=3:
	print("<usage>:<run> <host> <port>")
	exit()

addrinfo = socket.getaddrinfo(sys.argv[1], None)[0]
sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)

sock.connect((sys.argv[1],int(sys.argv[2])))

while True:
	print("Type ",end='')
	s = input()
	sock.send(s.encode())
	if s=="exit":
		break
	inp = sock.recv(1024)
	print("Received "+inp.decode())

print("Connection closed")
sock.close()