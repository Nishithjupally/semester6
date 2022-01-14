#!/bin/usr/env python3
import socket
import ssl
import os
import sys

if len(sys.argv)!=3:
	print("<usage>: <run> <host> <port>")
	exit()

host = sys.argv[1]
port = int(sys.argv[2])
addrinfo = socket.getaddrinfo(sys.argv[1], None)[0]
sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)
sock.setblocking(1)                     #no interruption

sock.connect((host, port))              #connect to the host and port

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)      
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations('server.pem')     #server verification
context.load_cert_chain(certfile="client.pem", keyfile="client.key")    

if ssl.HAS_SNI:
    secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=host)
else:
    secure_sock = context.wrap_socket(sock, server_side=False)          #handsahek

cert = secure_sock.getpeercert()

print(cert)			#printing certificate
print("\n\n")

print("Type: ",end='')
messg = input()
secure_sock.write(messg.encode())             #secure send receive
print("Received " +secure_sock.read(1024).decode())
print("Connection closed")               
secure_sock.close()
sock.close()