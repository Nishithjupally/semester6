#! /usr/bin/env python3
import sys
import os
import socket
import threading
import ssl
import time
import datetime


client_name = []

def sock_4(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)				#ipv4
	sock.bind(('',port))								#on local host
	sock.listen(5)
	return sock


def sock_6(port):
	sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
	sock.bind(('',port))								#on local host
	sock.listen(5)
	return sock

def echo_main(sock):
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
			print("Connection close\n")
			connect.close()
		except socket.timeout:
			print("Connection closed")
			print("Connection Timeout")
			break 

def echo(number,port):
	print("Echo mode")
	if number==4:
		sock = sock_4(port)
		echo_main(sock)
	elif number==6:
		sock = sock_6(port)
		echo_main(sock)
	return 

def file_main(sock):
	while True:
		sock.settimeout(25.0)
		try:
			while True:
				cli, addr = sock.accept() 
				print("Connected to "+addr[0] +" "+str(addr[1]))     
				filename2 = cli.recv(1024).decode()
				filename = filename2 + "_recv"
				f = open(filename,'wb')
				s = cli.recv(1024)
				while (s):
					f.write(s)
					s = cli.recv(1024)
					break
				print(f"Received {filename2} file \n")
			f.close()
			cli.close()
			sock.close()
		except socket.timeout:
			print("Connection closed")
			print("Connection Timeout")
			break
	return

def file(number,port):
	if number==4:
		sock = sock_4(port)
		file_main(sock)
	elif number==6:
		sock = sock_6(port)
		file_main(sock)
	return 

def ssl_echo_main(sock,port):
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', port))
	sock.listen(5)
	sock.settimeout(25)
	try:
		cli, addr = sock.accept()
	except socket.timeout:
		print("Time out")
		exit()
	secure_sock = ssl.wrap_socket(cli, server_side=True, ca_certs = "client.pem", certfile="server.pem", keyfile="server.key", cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1_2)
	cert = secure_sock.getpeercert()
	print("Secure Connection established with " + addr[0] + ":" + str(addr[1])+"\n")
	try:
		data = secure_sock.read(1024).decode()
		print(data)
		secure_sock.send(data.encode())
	finally:
		secure_sock.close()
		sock.close()
	print("\nConnection closed")

def ssl_echo(number,port):
	if number==4:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssl_echo_main(sock,port)
	elif number==6:
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		ssl_echo_main(sock,port)

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

def chat_server_main(sock,ip,port):
	sock.bind((ip, port))
	sock.listen(20)
	while True:
		conn, addr = sock.accept()
		client_name.append(conn)
		thr = threading.Thread(target = client_receive,args = (conn,addr,))
		thr.start()
		print (addr[0] + ":" + str(addr[1]) + " connected")
	conn.close()
	sock.close()
def chat_server(number,ip,port):
	if number==4:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		chat_server_main(sock,ip,port)
	elif number==6:
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		chat_server_main(sock,ip,port)
		
def main():
	if len(sys.argv)==4:
		number = 1
		if sys.argv[2]=='-4':
			number = 4
			port = (int)(sys.argv[3])
		elif sys.argv[2]=='-6':
			number = 6
			port = (int)(sys.argv[3])
		else:
			print("Provide correct arguments")
			exit()

		if sys.argv[1]=="-e":		
			echo(number,port)
		elif sys.argv[1]=="-f":
			file(number,port)
		elif sys.argv[1]=="-ssl":
			ssl_echo(number,port)
		else:
			print("Provide correct arguments")
			exit()
	
	elif len(sys.argv)==5:
		number =1;
		if sys.argv[2]=="-4":
			number=4
			ip = sys.argv[3]
			port = int(sys.argv[4])
		elif sys.argv[2]=="-6":
			number=6
			ip = sys.argv[3]
			port = int(sys.argv[4])
		else:
			print("Provide correct arguments")
			exit()

		if sys.argv[1]=="-ssl":
			ssl_echo(number,ip,port)
		elif sys.argv[1]=="-chat":
			chat_server(number,ip,port)
		else:
			print("Provide correct arguments")
			exit()
	else:
		print("Provide correct arguments")
		exit()

if __name__ == '__main__':
	main()