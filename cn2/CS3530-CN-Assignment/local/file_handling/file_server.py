#! /usr/bin/env python3  
import socket
import os
import tqdm
import getopt
import sys

SEPARATOR = "<SEPARATOR>"
if len(sys.argv)!=3:
    print("<usage>: <run> <-4/6> <port>")
    exit()

if sys.argv[1]=="-4":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

       
port = int(sys.argv[2])                
sock.bind(('', port))        
sock.listen(10)               
  
while True:  
    cli, addr = sock.accept() 
    print("Connection established "+ str(addr))     
    filename = cli.recv(1024).decode()
#    filename = "recv_" + filename          to remove confusion as in same folder
    f = open(filename,'wb')
    s = cli.recv(1024)
    while (s):
        f.write(s)
        s = cli.recv(1024)
    break
print(f"{filename} received")
f.close()
cli.close()
sock.close()
#only one file receiving