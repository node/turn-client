#!/usr/bin/python
'''
python UDP echo server by Chris <nodexy@gmail>
USAGE: %s <server_ip> <server_port>
'''

# 2012-2-22 Shenzhen, China
#

from SocketServer import DatagramRequestHandler, UDPServer
from sys import argv

class EchoHandler(DatagramRequestHandler):
    def handle(self):
        print "\nClient connected:", self.client_address
        message = self.rfile.read()
	print 'recv data: ',message
        self.wfile.write(message)
	print 'resp data: ',message

print '>> start '

if __name__ == '__main__':
    if len(argv) != 3:
        print __doc__ % argv[0]
    else:
        UDPServer((argv[1],int(argv[2])), EchoHandler).serve_forever()

print '<<end!'

