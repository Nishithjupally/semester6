#!/usr/bin/env python3
import socket
import os
import sys
import threading




def general(sock):
	sock.listen(5)
	while True:
		connect, addr = sock.accept()
		print("Connected to ",str(addr))
		while True:
			st = connect.recv(1024).decode()
			if st:
				print(str(addr)+":"+st)
				connect.send(st.encode())
			else:
				print("Connection closed "+str(addr))
				break
		connect.close()
	sock.close()




if len(sys.argv)!=2:
	print("<usage>: <run> <port>")
	exit()

sock1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock1.bind(('',int(sys.argv[1])))
sock2 = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
sock2.bind(('::1',int(sys.argv[1])))

th1=threading.Thread(target=general,args=(sock1,))
th2=threading.Thread(target=general,args=(sock2,))
th1.start()
th2.start()
