#!/usr/bin/python
#-*-  coding: UTF-8 -*-
'''
STUN(RFC5389) client demo by Chris <nodexy@gmail>
USAGE:
\t%s  <STUN_server_ip>  [STUN_server_port | 3478] [ <local_ip> <local_port | 7878>]
'''

#
# 2012-2-25 AT Shenzhen, China
# 2012-2-27 version 0.1 
#

# TODO: 
#    - send binging request again 
#

## parse CLI 
from sys import argv
import sys

if len(argv)!=2 and len(argv)!=3 and len(argv)!=5:
    print __doc__ % argv[0]
    sys.exit()

# default configuration 
host = argv[1]  #"192.168.0.181"  
port = 3478
local_ip = '192.168.0.75'
local_port = 7878
if len(argv)==3:
    port = int(argv[2])
    
if len(argv)==5:
    local_ip = argv[3]
    local_port = int(argv[4])

## STUN method & class & attribute
STUN_MAGIC_COOKIE = 0x2112A442
STUN_method={'STUN_METHOD_BINDING':0x0001}

STUN_class={
           'STUN_REQUEST':     0x0000,
           'STUN_SUCCESS_RESP':0x0100,
           'STUN_ERROR_RESP':  0x0110,
           'STUN_INDICATION':  0x0010
           }

def IS_REQUEST(msg_class):      return (((msg_class) & 0x0110) == 0x0000)
def IS_SUCCESS_RESP(msg_class): return (((msg_class) & 0x0110) == 0x0100)
def IS_ERR_RESP(msg_class):     return (((msg_class) & 0x0110) == 0x0110)
def IS_INDICATION(msg_class):   return (((msg_class) & 0x0110) == 0x0010)
def STUN_GET_METHOD(msg_type):  return ((msg_type) & 0x3EEF)
def STUN_GET_CLASS(msg_type):   return ((msg_type) & 0x0110)
def STUN_IS_COMPREHENSION_REQUIRED(attr_type):  return  (not((attr_type) & 0x8000))
def STUN_IS_COMPREHENSION_OPTIONAL(attr_type):  return  (((attr_type) & 0x8000))

STUN_ATTR_MAPPED_ADDRESS    = 0x0001
STUN_ATTR_USERNAME          = 0x0006
STUN_ATTR_MESSAGE_INTEGRITY = 0x0008
STUN_ATTR_ERROR_CODE        = 0x0009
STUN_ATTR_UNKNOWN_ATTRIBUTES= 0x000A
STUN_ATTR_REALM             = 0x0014
STUN_ATTR_NONCE             = 0x0015
STUN_ATTR_XOR_MAPPED_ADDRESS= 0x0020
STUN_ATTR_SOFTWARE          = 0x8022
STUN_ATTR_ALTERNATE_SERVER  = 0x8023
STUN_ATTR_FINGERPRINT       = 0x8028

## utility 
# generate transaction ID
import random
def genTranID():
    a = ''.join([random.choice('0123456789ABCDEF') for x in xrange(32)])
    return binascii.a2b_hex(a)
    #return a

# parse received response packet
def recv_resp(buf): 
    msgType = int(binascii.b2a_hex(buf[0:2]),16)
    msgLength = int(binascii.b2a_hex(buf[2:4]),16)
    magic_cookie = binascii.b2a_hex(buf[4:8])
    transId = binascii.b2a_hex(buf[8:20])
    
    header = (msgType,msgLength,magic_cookie,transId)
    
    print '\n>>header: '
    print hex(msgType),msgLength,magic_cookie,transId
    if IS_SUCCESS_RESP(msgType):
        pass #print 'Success resp'
    elif IS_ERR_RESP(msgType):
        print 'Error resp'
    else:
        print 'Unknown msg type'
    
    print '>>attrs:'
    attrs = []
    len_remain = msgLength
    base = 20
    while len_remain>=4:
        attr_type = int(binascii.b2a_hex(buf[base:(base+2)]),16)
        attr_len = int(binascii.b2a_hex(buf[(base+2):(base+4)]),16)
        attr_value = binascii.b2a_hex(buf[base+4:base+4+attr_len])
        
        if attr_type ==  STUN_ATTR_XOR_MAPPED_ADDRESS: # 0x0020 
            port = 0x2112 ^ int(binascii.b2a_hex(buf[base+6:base+8]), 16)
            tip =[1,2,3,4]
            tip[0] = 0x21 ^ int(binascii.b2a_hex(buf[base+8:base+9]), 16)
            tip[1] = 0x12 ^ int(binascii.b2a_hex(buf[base+9:base+10]), 16)
            tip[2] = 0xA4 ^ int(binascii.b2a_hex(buf[base+10:base+11]), 16)
            tip[3] = 0x42 ^ int(binascii.b2a_hex(buf[base+11:base+12]), 16)
            ip = '.'.join([str(x) for x in tip])            
            
            attrs.append([attr_type,ip+':'+str(port)])
            print attr_type, ip,':',port,' (XOR=',attr_value,')'
        else:
            attrs.append([attr_type,attr_value])
            print attr_type,str(int(attr_value,16))
        
        base = base + 4 + attr_len
        len_remain = len_remain - (4+attr_len)
    
    #print 'body: ',attrs
    
    return (header,attrs)

## connect STUN server
import socket
import struct
import binascii
 

## first bind 
def stun_binding_first(sock):
    print '\nSTUN binding request ...'
    # header
    header = struct.pack('!H',STUN_method['STUN_METHOD_BINDING']) # binding req
    header += struct.pack('!H',0x0000)               # length
    header += struct.pack('!l',STUN_MAGIC_COOKIE)    # magic cookie
    header += struct.pack('!32s',genTranID())        # trans ID
    # body 
    body = struct.pack('!H',0x8022)           # software   
    body += struct.pack('!h',0x0014)          # length
    body += struct.pack('!20s','PY STUN CLIENT 0.1')#value
    # msg
    send_data = header #+ body # TODO 
    
    
    print 'Send data ...'
    r = sock.sendto(send_data,(host,port))
    print 'size=',r
        
    print 'Recv data ...'
    buf,address = sock.recvfrom(1024)
    print 'size=',len(buf)
    
    print 'data: ',buf
    print 'from: ',address
    
    (header,attr) = recv_resp(buf)
    
    # TODD: parse: realm, nonce 
    print ''
    return (header,attr)

## bind again 
def stun_binding_again(sock):
    pass
    # TODO: parse: xor-mapped-address 


if __name__ == '__main__':
    print 'STUN(RFC5389) client demo by Chris <nodexy@gmail>\n'
    
    print 'Connect to server  : ',host,port
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print 'Bind local ip:port : ',local_ip,local_port
    sock.bind((local_ip,local_port))

    # binding first 
    msg = stun_binding_first(sock)
    

    got_XOR_MAPPED_ADDR = False
    XOR_MAPPED_ADDR = None
    for x in msg[1]:
        if x[0]== STUN_ATTR_XOR_MAPPED_ADDRESS:
            got_XOR_MAPPED_ADDR = True
            XOR_MAPPED_ADDR = x[1]
            break;

    if got_XOR_MAPPED_ADDR:
        print '>>> Success! XOR-MAPPED-ADDRESS=',XOR_MAPPED_ADDR
    else:
        print '>>> First binding error ,and try again ...'
        pass 
        # TODO: msg = stun_binding_again(sock)
        
    print 'END!'

#END