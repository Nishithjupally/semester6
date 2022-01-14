#!/usr/bin/env python3
import socket
import sys
import os
import datetime

if len(sys.argv)!=3:
	print("<usage>:<run> <host> <port>")
	exit()
addrinfo = socket.getaddrinfo(sys.argv[1], None)[0]
sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)
sock.connect((sys.argv[1],int(sys.argv[2])))

while True:							
	print("Type: ",end='')
	s = input()	
	if s=="exit":
		break
	t = datetime.datetime.now().strftime("%H:%M:%S")				#sending the time stamp as well
	s = s  + " at "+ t																
	sock.send(s.encode())
	ans = sock.recv(1024)
	print("Received: "+ans.decode()+"\n")
sock.close()						