#!/usr/bin/python3

# connects to server.py and transfers the IP database to /var/tmp/ip.db

import socket
import time

# digital ocean vm - 67.205.131.5
TCP_IP = '67.205.131.5'
TCP_PORT = 55555

BUFFER_SIZE = 1024

# opening a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting to the TCP_IP '67.205.131.5' at port 55555
s.connect((TCP_IP, TCP_PORT))
# define variables used to calculate file transfer time
clock_start = time.clock()
time_start = time.time()
# opening file where we will write the data (binary mode SQLite DB file)
with open('/var/tmp/ip.db', 'wb') as f:
    print('file opened')
    # open file Success? go further
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        #print('data=%s', (data))
        if not data:
            # closing the file
            f.close()
            print('file close()')
            break
        # write data to a file
        f.write(data)

print('File transfer successful')

# closing a socket
s.close()
print('connection closed')
# clock ends here 
clock_end = time.clock()
time_end = time.time()
# calculating the clock duration for analysing the data and printing
duration_clock = clock_end - clock_start
print('clock:  start = ',clock_start, ' end = ',clock_end)
print('clock:  duration_clock = ', duration_clock)
# calculating the time duration for analysing the data and printing
duration_time = time_end - time_start
print('time:  start = ',time_start, ' end = ',time_end)
print('time:  duration_time = ', duration_time)

