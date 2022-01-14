#! /usr/bin/env python3
import sys
import os
import socket
import threading
import datetime
import time
import ssl


flag =0

def sock_4(ip,port):
	addrinfo = socket.getaddrinfo(ip, None)[0]
	sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)
	sock.connect((ip,port))
	print("Connected to "+ip + " "+str(port))
	return sock

def sock_6(ip,port):
	addrinfo = socket.getaddrinfo(ip, None)[0]
	sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)
	sock.connect((ip,port))								#on local host
	print("Connected to "+ip + " "+str(port))
	return sock


def echo_main(sock):
	print("Type: ",end='')
	s = input()
	t = datetime.datetime.now().strftime("%H:%M:%S")
	s = s + " at " + t
	sock.send(s.encode())
	ans = sock.recv(1024)
	print("Received: "+ans.decode())
	print("Connection closed")
	sock.close()	
	return

def echo(number,ip,port):
	if number==4:
		sock = sock_4(ip,port) 
		echo_main(sock)
	elif number==6:
		sock = sock_6(ip,port)
		echo_main(sock)
	return 
# send this to the server and get it back


def echo_loop_main(sock):
	while True:
		print("Type: ",end='')
		s = input()
		if s=="exit":
			break
		t = datetime.datetime.now().strftime("%H:%M:%S")
		s = s  + " at "+ t
		sock.send(s.encode())
		ans = sock.recv(1024)
		print("Received: "+ans.decode()+"\n")
	sock.close()
	return 

def echo_loop(number,ip,port):
	if number==4:
		sock = sock_4(ip,port)
		echo_loop_main(sock)
	elif number==6:
		sock = sock_6(ip,port)
		echo_loop_main(sock)						
	return 

def file_main(sock,filename):
	sock.send(f"{filename}".encode())
	time.sleep(1)
	f = open(filename,"rb")
	s = f.read(1024)
	while(s):
		sock.send(s)
		s = f.read(1024)
	print(f"{filename} transfer done")
	sock.close()
	return 	

def file(number,ip,port,filename):
	filesize = os.path.getsize(filename)
	if number==4:
		sock = sock_4(ip,port)
		file_main(sock,filename)
	elif number==6:
		sock = sock_6(ip,port)
		file_main(sock,filename)
	return

def info(hostname,port):
	addrinfo = socket.getaddrinfo(hostname,port)
	if hostname=="localhost":
		print("ipv-4 address= " + str(addrinfo[0][4][0]))
		print("port= " + str(addrinfo[0][4][1]))	
		print("\nAddrinfo Result")
		print(addrinfo)
		return
	elif hostname=="ip6-localhost":
		print("ipv-6 address= " + str(addrinfo[0][4][0]))
		print("port= " + str(addrinfo[0][4][1]))	
		print("\nAddrinfo Result")
		print(addrinfo)										#local info
		return 											#other cases
	print("ipv-4 address= " + str(addrinfo[0][4][0]))
	print("port= " + str(addrinfo[0][4][1]))
	print("ipv-6 address= " + str(addrinfo[4][4][0]))
	print("port= " + str(addrinfo[4][4][1]))
	print("\nAddrinfo Result")
	print(addrinfo)

def echo_message_ssl(sock):
	print("Type: ",end='')
	s = input()
	t = datetime.datetime.now().strftime("%H:%M:%S")
	s = s + " at " + t
	sock.send(s.encode())
	ans = sock.recv(1024)
	print("Received: "+ans.decode()+"\n")	
	return
def ssl_echo_main(sock,ip,port):
	sock.setblocking(1)
	sock.connect((ip, port))
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.verify_mode = ssl.CERT_REQUIRED
	context.load_verify_locations('server.pem')
	context.load_cert_chain(certfile="client.pem", keyfile="client.key")
	if ssl.HAS_SNI:
		secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=ip)
	else:
		secure_sock = context.wrap_socket(sock, server_side=False)
	cert = secure_sock.getpeercert()
	print("Secure Connection established with " + ip + "\n")
	echo_message_ssl(secure_sock)
	secure_sock.close()
	sock.close()
	print("Connection closed")

def ssl_echo(number,ip,port):
	if number==4:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssl_echo_main(sock,ip,port)
	elif number==6:
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		ssl_echo_main(sock,ip,port)

def recv_from_serv(cli):
	while True:
		try:
			data = cli.recv(1024).decode()
			if data:
				print(data)
			else:
				print("Connection ended")
				return 
		except:
			continue

def chat_client_main(cli,ip,port):
	cli.connect((ip,int(port)))
	print("Client connected to server")
	messg_thread = threading.Thread(target= recv_from_serv, args=(cli,))
	messg_thread.start()					#to read and send the messages accordingly
	flag = 0
	while True:
		s = input()
		cli.send(s.encode())
	print("Connection closed")
	cli.close()
	return


def chat_client(number,ip,port):
	if number==4:
		cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		chat_client_main(cli,ip,port)
	elif number==6:
		cli = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
		chat_client_main(cli,ip,port)
	return 	
def main():
	if len(sys.argv)==6:
		number = 1
		if sys.argv[3]=='-4':
			number = 4
			ip = sys.argv[4]
			port = (int)(sys.argv[5])
		elif sys.argv[3]=='-6':
			number = 6
			ip = sys.argv[4]
			port = (int)(sys.argv[5])
		else:
			print("Provide correct arguments")
			exit()

		if sys.argv[1]=="-e":		#echo client
			if sys.argv[2]=="-s":			#single 
				echo(number,ip,port)		#loop
			elif sys.argv[2]=="-l":		
				echo_loop(number,ip,port)
			elif sys.argv[2]=="-ssl":
				ssl_echo(number,ip,port)
			else:
				print("Provide correct arguments")
				exit()
		elif sys.argv[1]=="-f":
			filename = sys.argv[2]
			file(number,ip,port,filename)
		else:
			print("Provide correct arguments")
			exit()

	elif len(sys.argv)==4:
		if sys.argv[1]=="-i":
			hostname = sys.argv[2]
			port = sys.argv[3]
			info(hostname,port)
		else:
			print("Provide correct arguments")
			exit()
	elif len(sys.argv)==5:
		if sys.argv[1]=="-chat":
			if sys.argv[2]=="-4":
				number=4
			elif sys.argv[2]=="-6":
				number=6
			else:
				print("Provide correct arguments")
				exit()
			chat_client(number,sys.argv[3],sys.argv[4])
		else:
			print("Provide correct arguments")
			exit()
	else:
		print("Provide correct arguments")
		exit()






if __name__ == '__main__':
	main()