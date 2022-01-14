#! /usr/bin/env python3
import socket
import os
import sys
import struct
import threading


def recv_from_serv(cli):
	while True:
		try:
			data = cli.recv(4096).decode()
			if data:
				print(data)
			else:
				print("Connection ended")
				flag = 1
				return 
		except:
			continue

if len(sys.argv)!=3:
	print("<usage>: <run> <ip> <port>")
	exit()

cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = str(sys.argv[1])
port = int(sys.argv[2])
flag = 0
cli.connect((host,port))
print("Client connected to server")

messg_thread = threading.Thread(target= recv_from_serv, args=(cli,))
messg_thread.start()					#to read and send the messages accordingly
while True:
	s = input()
	cli.send(s.encode())
	if flag==1:
		break
cli.close()