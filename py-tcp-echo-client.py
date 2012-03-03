#!/usr/bin/python
'''
python TCP echo client by Chris <nodexy@gmail>
USAGE: %s <server_ip> <server_port> <msg>
'''

# 2012-2-22 Shenzhen, China

import socket
from sys import argv

def f(host,port,msg):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))

    sock.send(msg)
    print 'send data: ',msg
    recv_msg = sock.recv(100)
    print 'recv data: ',recv_msg


    sock.close()





print '>>start'

if __name__ == '__main__':
    if len(argv)!=4:
        print __doc__ % argv[0]
    else:
        f(argv[1],int(argv[2]),argv[3])

print '>>END!'
