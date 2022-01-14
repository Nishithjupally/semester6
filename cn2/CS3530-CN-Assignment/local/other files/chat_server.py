#! /usr/bin/env python3
import socket
import sys
import threading

def client_receive(conn, addr): 
	conn.send("Welcome!".encode())
	while True:
			try:
				message = conn.recv(1024).decode()
				if message:
					print ( addr[0] + ":" + str(addr[1]) + " "+ message)
					s = addr[0] + ":" + str(addr[1]) + " "+ message
					send_to_all(s, conn)
				else:
					dlt(conn)
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
  

if len(sys.argv) != 3:
	print ("<usage>: <run> <ip> <port>")
	exit()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = str(sys.argv[1])
port = int(sys.argv[2])

sock.bind((host, port))
sock.listen(20)

client_name = []
while True:
	conn, addr = sock.accept()
	client_name.append(conn)
	thr = threading.Thread(target = client_receive,args = (conn,addr,))
	thr.start()
	print (addr[0] + str(addr[1]) + " connected")

conn.close()
sock.close()