# 套接字
## TCP/IP协议簇的套接字地址可以采用以下的结构
```c
#include<netinet /in.h>
#include<sys/socket.h>

struct in_addr
{
    _u32 s_addr;                    /* UINT类型 */
}

struct sockaddr_in
{
    short int sin_family;           /* 地址类型：AF_XXX */
    unsigned short int sin_port;    /* 端口号 */
    struct in_addr sin_addr;        /* Internet地址 */
    unsigned char sin_zero[8];
};
unsigned char__pad[__SOCKET_SIZE__-sizeof(short int)-sizeof(unsigned short int)-sizeof(struct in_addr)];
}

#define sin_zero__pad
```