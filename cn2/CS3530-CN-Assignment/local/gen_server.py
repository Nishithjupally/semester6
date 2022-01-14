#! /usr/bin/env python3
import socket
import sys
import os

sock = socket.socket()				#ipv4

sock.bind(('',12345))								#on local host
sock.listen(5)

print("-----")
while True:
    connect, addr = sock.accept()
    print(addr)
    print("Connected to " + addr[0] + " " + str(addr[1]))
    while True:
        s = connect.recv(1024)
        if s:
        	print(str("Message from " + addr[0]) + " : " + s.decode())
        	connect.send(s)
        else:
        	break
    connect.close()