#!/usr/bin/python
'''
python TCP echo sever by Chris <nodexy@gmail>
USAGE: %s <server_ip> <server_port>
'''

# 2012-2-22 Shenzhen, China

import socket
from sys import argv


def f(host,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen(10)

    while True:
        conn,client = sock.accept()
        print '\nnew client: ',client
        data = conn.recv(1024)
        print 'recv data: ',data
        if data:
            conn.send(data)
            print 'resp data: ',data
        
    sock.close()



print '>>start '

if __name__ == '__main__':
    if len(argv) != 3:
        print __doc__ % argv[0]
    else:
        f(argv[1],int(argv[2]))


print '>>end!'
