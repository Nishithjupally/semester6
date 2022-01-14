#! /usr/bin/env python3
import socket
import os
import tqdm
import getopt
import threading
import sys
import time
							#importing libraries
if len(sys.argv)!=4:
	print("<usage>: <run> <file name> <host> <port>")
	exit()

host = sys.argv[2]
port = int(sys.argv[3])
filename = str(sys.argv[1])		#input the file name in the directory to transfer it
filesize = os.path.getsize(filename)
addrinfo = socket.getaddrinfo(sys.argv[1], None)[0]
sock = socket.socket(addrinfo[0],socket.SOCK_STREAM)
sock.connect((host,port))	
print(f"Connected to {host}:{port}")
sock.send(f"{filename}".encode())	#sending the file name
time.sleep(0.8)
f = open(filename,"rb")				#open the file and read in binary format 
s = f.read(1024)
while(s):
	sock.send(s)					#send the data 
	s = f.read(1024)				#read again and until data is over
print(f"{filename} transfer done")
sock.close()						#close the socket