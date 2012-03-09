#!/usr/bin/python
#-*- coding: UTF-8 -*-
'''
python UDP ping tool by Chris <nodexy@gmail>
USAGE:
\t%s <remote_ip:remote_port> [ping_count]
'''

# 2012-3-8 Shenzhen,China 
# 

from sys import argv
import sys

if len(argv) != 2 and len(argv) != 3:
	print __doc__ % argv[0]
	sys.exit()

remote_host = ('192.168.123.128',9800)
#local_host  = ('192.168.123.128',9801)
n = 5
data_bytes = 32
data = ''.join(['*' for x in range(data_bytes)])

remote_ip_port = argv[1].split(':')
if len(remote_ip_port)!=2:
	print __doc__ % argv[0]
	sys.exit()
remote_host = (remote_ip_port[0],int(remote_ip_port[1]))
if len(argv) == 3:
	n = int(argv[2])

import socket
import time
socket.setdefaulttimeout(3)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.bind(local_host)

print ''
print 'Ping ',remote_host,' with %d bytes of data:' % data_bytes
print ''

send_n = 0
recv_n = 0
lost_n = 0
tt = []

for x in range(1,n+1):
	t0 = time.time()
	try:
		n = sock.sendto(data,remote_host)
		print 'Ping %d bytes=%d ; ' % (x,n) ,
		send_n += 1
	
		t0 = time.time()
		d,addr = sock.recvfrom(1024)
		t1 = time.time()-t0
		print 'Reply from ',addr,' bytes=%d time=%dms ' % (len(d),t1)
		recv_n += 1
		tt.append(t1)
	except socket.error, msg:
		print 'Recvfrom except : ', msg, ' time=%dms ' % (time.time()-t0)
		lost_n += 1

	time.sleep(0.5)

print ''
print 'Ping statistics for ' ,remote_host,':'
if send_n>0:
	print '\tPackes: Sent = %d, Received = %d,  Lost = %d (%d%% loss)  ,' % (send_n,recv_n,lost_n,lost_n*100/send_n)
else:
	print 'None.'
print 'Approximate round trip times in milli-seconds:'
if tt:
	print '\tMinimum = %dms, Maximum = %dms, Average = %dms' % (min(tt),max(tt),sum(tt)/len(tt))
else:
	print '\tNone.'
print ''

# END 