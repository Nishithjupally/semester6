#!/usr/bin/env python3
import time
import struct
import socket
import sys
import threading
import datetime

port = 12345
ipv4 = '224.0.0.251'
ipv6 = 'ff02::fb'
mttl = 1 

def echo_main(sock,addrinfo):
    while True:
        print("Type: ",end='')
        s = input()
        if s=="exit":
            break
        t = datetime.datetime.now().strftime("%H:%M:%S")
        s = s + " at " + t
        sock.sendto(s.encode(),(addrinfo[4][0],port))
    sock.close()
    return

def sender(group):
    addrinfo = socket.getaddrinfo(group, None)[0]
    sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    ttl_bin = struct.pack('@i', mttl)
    if addrinfo[0] == socket.AF_INET: 
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    else:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
    echo_main(sock,addrinfo)
    print("Connection closed")


def receiver(group):
    addrinfo = socket.getaddrinfo(group, None)[0]
    sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    if addrinfo[0] == socket.AF_INET: 
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    sock.settimeout(20)
    while True:
        try:
            data, sender = sock.recvfrom(1024) 
            print (str(sender) + '  ' + data.decode())
        except socket.timeout:
            print("No sender")
            print("Listening Timeout")
            break


def main():
    if len(sys.argv)<3:
        print("<usage>: <run> <-s/-r> <-4/-6>")
        exit()
    if sys.argv[2]=="-6":
        group = ipv6
    elif sys.argv[2]=="-4":
        group = ipv4
    else:
        print("<usage>: <run> <sender/receiver> <ipv4/ipv6>")
            
    if sys.argv[1]=="-s":       
        sender(group)              #sender
    elif sys.argv[1]=="-r":
        receiver(group)         #reciver
    else:
        print("<usage>: <run> <sender/receiver> <ipv4/ipv6>")


if __name__ == '__main__':
    main()
