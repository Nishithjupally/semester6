#!/usr/bin/env python3
import socket
import sys
import os

sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)

sock.connect(('ip6-localhost',12345))

while True:
	while True:						# send this to the server and get it back
		print("Type: ")
		s = input()
		sock.send(s.encode())
		ans = sock.recv(1024)
		print("Received: "+ans.decode())
		break
	break
sock.close()