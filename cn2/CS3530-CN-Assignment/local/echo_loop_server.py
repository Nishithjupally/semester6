#! /usr/bin/env python3
import socket
import sys
import os

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind(('127.0.0.1',12345))
sock.listen(5)
print("-----")
while True:
	sock.settimeout(25.0)
	try:
		connect, addr = sock.accept()
		print("Connected to " + addr[0] + " " + str(addr[1]))
		while True:
			s = connect.recv(1024)
			if s:
				print(str("Message from " + addr[0]) + " : " + s.decode())
				connect.send(s)
			else:
				break
		connect.close()
	except socket.timeout:
		print("Connection Timeout")
		break