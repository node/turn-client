#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

/*
*
* STUN(RFC5389) client api by Chris <nodexy@gmail>
* 
* Test by turnserver-0.6 from http://turnserver.sourceforge.net
*
* @ 2012-2-28 Shenszhen, China
* @ 2012-2-29 version 0.1
*/


int stun_xor_addr(int sockfd,char * stun_server_ip,unsigned short stun_server_port, char * return_ip, unsigned short * return_port);



int main(int argc, char *argv[])
{
        if (argc != 4) {
		printf("STUN(RFC5389) client api by Chris <nodexy@gmail>\n");
                printf("usage: %s <server_ip> <server_port> <local_port>\n\n", argv[0]);
                exit(1);
        }


        printf("Main start ... \n");

        struct sockaddr_in localaddr;
	int n;

	int sockfd;
	char return_ip[32]; 
	unsigned short return_port=0;
	
        //# create socket
        sockfd = socket(AF_INET, SOCK_DGRAM, 0); // UDP


        // local
        bzero(&localaddr, sizeof(localaddr));
        localaddr.sin_family = AF_INET;
        localaddr.sin_port = htons(atoi(argv[3]));

	n = bind(sockfd,(struct sockaddr *)&localaddr,sizeof(localaddr));
        //printf("bind result=%d\n",n);

        printf("socket opened to  %s:%s  at local port %s\n",argv[1],argv[2],argv[3]);


	n = stun_xor_addr(sockfd,argv[1],(unsigned short)atoi(argv[2]),return_ip,&return_port);
	if (n!=0)
		printf("STUN req error : %d\n",n);
	else
		printf("ip:port = %s:%d\n",return_ip,return_port);

	printf("main over.\n");

}

int stun_xor_addr(int sockfd,char * stun_server_ip,unsigned short stun_server_port,char * return_ip, unsigned short * return_port)
{
	struct sockaddr_in servaddr;
	unsigned char buf[300];
	int i;
        unsigned char bindingReq[20];    

	int stun_method,msg_length;
	short attr_type;
	short attr_length;
	short port;
	short n;

	// server
        bzero(&servaddr, sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        inet_pton(AF_INET, stun_server_ip, &servaddr.sin_addr);
        servaddr.sin_port = htons(stun_server_port);	


        //## first bind 
	* (short *)(&bindingReq[0]) = htons(0x0001);    // stun_method
	* (short *)(&bindingReq[2]) = htons(0x0000);    // msg_length
	* (int *)(&bindingReq[4])   = htonl(0x2112A442);// magic cookie

	*(int *)(&bindingReq[8]) = htonl(0x63c7117e);   // transacation ID 
	*(int *)(&bindingReq[12])= htonl(0x0714278f);
	*(int *)(&bindingReq[16])= htonl(0x5ded3221);



        //printf("Send data ...\n");
        n = sendto(sockfd, bindingReq, sizeof(bindingReq),0,(struct sockaddr *)&servaddr, sizeof(servaddr)); // send UDP
	if (n == -1)
	{
		printf("sendto error\n");
		return -1;
	}
	// time wait
	usleep(1000 * 100);

        //printf("Read recv ...\n");
        n = recvfrom(sockfd, buf, 300, 0, NULL,0); // recv UDP
        if (n == -1)
	{
	    printf("recvfrom error\n");
	    return -2;
	}
	//printf("Response from server:\n");
	//write(STDOUT_FILENO, buf, n);

	if (*(short *)(&buf[0]) == htons(0x0101))
	{
		//printf("STUN binding resp: success !\n");

		// parse XOR
		n = htons(*(short *)(&buf[2]));
		i = 20;
        	while(i<sizeof(buf))
       	 	{
                	attr_type = htons(*(short *)(&buf[i]));
			attr_length = htons(*(short *)(&buf[i+2]));
			if (attr_type == 0x0020)
			{
				// parse : port, IP 

				port = ntohs(*(short *)(&buf[i+6]));
				port ^= 0x2112;
				//printf("@port = %d\n",(unsigned short)port);

				

				/*printf("@ip   = %d.",buf[i+8] ^ 0x21);
				printf("%d.",buf[i+9] ^ 0x12);
				printf("%d.",buf[i+10] ^ 0xA4);
				printf("%d\n",buf[i+11] ^ 0x42);
				*/		
	
				// return 
				*return_port = port;
				sprintf(return_ip,"%d.%d.%d.%d",buf[i+8]^0x21,buf[i+9]^0x12,buf[i+10]^0xA4,buf[i+11]^0x42);

	
				break;
			}
			i += (4  + attr_length);


        	}

	}


	// do not close the socket !!!

	return 0;
}
