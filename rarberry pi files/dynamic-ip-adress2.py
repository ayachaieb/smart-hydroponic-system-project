#!/usr/bin/python3
import socket
import os
def ipadress():
	gw = os.popen("ip -4 route show default").read().split()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((gw[2], 0))
	ipaddr = s.getsockname()[0]
	gateway = gw[2]
	host = socket.gethostname()
#	print ("IP:", ipaddr, " GW:", gateway, " Host:", host)
	print(ipaddr)
	return(ipaddr)
ipadress()
