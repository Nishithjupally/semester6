#! /usr/bin/env python3
import socket
import sys
import threading
import time

def client_receive(conn, addr): 
	conn.send("Welcome!".encode())
	while True:
			try:
				message = conn.recv(2048).decode()
				if message:
					print ( addr[0] + ":" + str(addr[1]) + " "+ message)
					s = addr[0] + ":" + str(addr[1]) + " "+ message
					send_to_all(s, conn)
				else:
					dlt(conn)
					print("Connection closed " + addr[0] +":" + addr[1])
			except:
				continue

def send_to_all(message, connec):
	for cli in client_name:
		if cli!=connec:
			try:
				cli.send(message.encode())
			except:
				cli.close()
				dlt(cli)


def dlt(connec):
	if connec in client_name:
		client_name.remove(connec)
  

if len(sys.argv) != 2:
	print ("<usage>: <run> <port>")
	exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
sock.bind(('', port))
sock.listen(20)
print("Server started\n")
client_name = []
while True:
	conn, addr = sock.accept()
	client_name.append(conn)
	thr = threading.Thread(target = client_receive,args = (conn,addr,))	#creating a thread
	thr.start()
	print (addr[0] + ":" + str(addr[1]) + " connected")
conn.close()
sock.close()