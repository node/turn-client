#!/usr/bin/python
'''
python UDP echo server by Chris <nodexy@gmail>
USAGE: %s <server> <port>
'''

# 2012-2-22 Shenzhen, China
#

import socket
from sys import argv

def f(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:

	# receive 
        data,client = sock.recvfrom(1024)
        if not data: 
            print 'client has existed: ',client
            continue #break
        print '\nrecv data from ',client,': ',data

	# response
	sock.sendto(data,client)
        print 'resp data to ',client,' : ',data

    sock.close()



print '>>Start ...'

if __name__ == '__main__':
    if len(argv) != 3:
        print __doc__ % argv[0]
    else:
        f(argv[1],int(argv[2]))

print '>>END!'

