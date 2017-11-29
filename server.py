#!/bin/python3.6

import socket
from threading import Thread
# Added import ThreadingMixIn as we wanted to allow multiple users to hit server in one go
from socketserver import ThreadingMixIn

# TCP_IP = 'localhost' i.e "172.19.72.81"
TCP_IP = socket.gethostbyaddr("172.19.72.81")[0]
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
        filename='mytext.txt'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

