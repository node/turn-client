#!/usr/bin/python
'''
python UDP echo client by Chris <nodexy@gmail> 
USAGE: %s <server_ip> <server_port> <message>
'''

# 2012-2-22 Shenzhen, China

import socket
import time
from sys import argv

def f(host,port,msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'connect to server: ',host,port  

    print 'send msg: ',msg
    sock.sendto(msg,(host,port))
    print 'recv msg: ',sock.recv(1024)

    sock.close()


print '>>>Start ...'
if __name__ == '__main__':
    if len(argv) !=4:
        print __doc__ % argv[0]
    else:
        f(argv[1],int(argv[2]),argv[3])

print '>>>END!'

