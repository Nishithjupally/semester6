#! /usr/bin/env python3
import socket
import sys
import os

if len(sys.argv)!=3:
    print("<usage>: <run> <type> <port>")
    exit()


if sys.argv[1]=="-4":
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
elif sys.argv[1]=="-6":
    sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)

sock.bind(('',int(sys.argv[2])))								#on local host
sock.listen(5)

print("-----")
while True:
    connect, addr = sock.accept()
    print("Connected to " + addr[0] + " " + str(addr[1]))
    while True:
        s = connect.recv(1024)
        if s:
        	print(str("Message from " + addr[0]) + " : " + s.decode())
        	connect.send(s)
        else:
        	break
    print("Connection closed\n")
    connect.close()