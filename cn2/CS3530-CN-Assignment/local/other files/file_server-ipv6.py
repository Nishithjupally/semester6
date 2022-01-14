#! /usr/bin/env python3  
import socket
import os
import tqdm
import getopt
import sys
import time	
						
sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)       	#support ipv6 and ipv4 as well in file transfer

port = 12345                
sock.bind(('2402:8100:2843:45a3:d705:5548:98c0:9e63', port))        	
  
sock.listen(50)
sock.settimeout(10)               	#set timeout for listen
print("Server listening")
while True:  
    try:
    	cli, addr = sock.accept()       
    	print("Connected to "+ addr[0] + " " + str(addr[1]))
    	filename = cli.recv(1024).decode()		#decode the data received
#    filename = filename + str(10) if in same directory then not to overlap
    	f = open(filename,'wb')
    	s = cli.recv(1024)
    	while (s):
        	f.write(s)					#get the data
        	s = cli.recv(1024)
    	f.close()		
    	cli.close()
    	print("File received")			
    	print("Connection closed to "+ addr[0] + " " + str(addr[1]))
    except socket.timeout:													#waiting until timeout of connection
    	print("Connection timeout")
    	break