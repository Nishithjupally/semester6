#!/bin/usr/env python3
import socket
import ssl
import pprint
import os
import sys

if len(sys.argv)!=3:
	print("<usage>: <run> <-4/6> <port>")
	exit()
	
port = int(sys.argv[2])
if sys.argv=="-4":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
	sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', port))
sock.listen(5)
cli, addr = sock.accept()   # cleint sends request, check the permissions accordingly
secure_sock = ssl.wrap_socket(cli, server_side=True, ca_certs = "client.pem", certfile="server.pem", keyfile="server.key", cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1_2)                

cert = secure_sock.getpeercert()
print(cert)		#printing the certificate
print("\n")
while True:
	secure_sock.settimeout(25)
	try:
		data = secure_sock.read(1024).decode()
		if data:
			print(data)
			secure_sock.write(data.encode())
		else:
			break
	except socket.timeout:
		print("Time out")
		break
print("Connection closed")
secure_sock.close()
sock.close()