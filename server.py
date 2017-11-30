#!/bin/python3.6

import socket
from threading import Thread
# Added import ThreadingMixIn as we wanted to allow multiple users to hit server in one go
# i.e. multithreaded:
from socketserver import ThreadingMixIn

# TCP_IP = 'localhost' i.e "172.19.72.81"
# TCP_IP = socket.gethostbyaddr("172.19.72.81")[0]
#
# Digital Ocean IP
TCP_IP = '67.205.131.5'
TCP_PORT = 55555
BUFFER_SIZE = 1024

print('TCP_IP=',TCP_IP)
print('TCP_PORT=',TCP_PORT)

# declaring a class which takes a thread as input 
class ClientThread(Thread):
# defining a constructor for thread
    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started for "+ip+":"+str(port))

    def run(self):
        # define filename/location
        # note this file is created by /usr/local/sbin/update_db.py on the HoneyPot
        filename='/var/tmp/ip.db'
        # open the file in binary mode
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break
                
# create a socket and call it tcpsock
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    # listen on the IP:Port and allow as many as 6 connections before refusing new connections
    tcpsock.listen(6)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

