#coding=utf-8
import random
import binascii
import argparse
import sys
import time

sys.setrecursionlimit(100000)   #设置迭代次数限制
 
def main():
    n,e,d=Build_key()     #生成公钥、密钥

    e = int(e,16)
    n = int(n,16)
    d = int(d,16)
    m = "WhatIlikeisthefuture"
    print("Encrypting......")
    start = time.clock()
    cipher = encrypt(m,e,n)
    print("Encrypted!\r\nThe Cipher is:",cipher)
    end1 = time.clock()
    print("加密用时："+str(end1-start))

    c = cipher     #读取密文
    print("Decrypting......")
    plain = decrypt(c,d,n)
    print("Decrypted!\r\nThe PlainText is:",plain)
    end2 = time.clock()
    print("解密用时："+str(end2-end1))
 
#平方—乘法，最后返回结果
def MRF(b,n,m):
    a=1
    x=b;y=n;z=m
    binstr = bin(n)[2:][::-1]   #通过切片去掉开头的0b，截取后面，然后反转
    for item in binstr:
            if item == '1':
                    a = (a*b)%m
                    b = (b**2)%m
            elif item == '0':
                    b = (b**2)%m
    return a
 
#素性检验
def MillerRabin(n):
    "利用Miller-Rabin算法检验生成的奇数是否为素数"
    m=n-1
    k=0
    while(m%2==0):
        m=m//2
        k=k+1
    a=random.randint(2,n)
    #b=a**m%n
    b = MRF(a,m,n)
    if(b==1):
        return 1
    for i in range(k):
        if(b==n-1):
            return 1
        else:
            b=b*b%n
    return 0
 
#生成大素数，20次MillerRabin算法缩小出错的概率
def BigPrime():
        Min = 10**11;Max = 10**15;p = 0
        while(1):
                p = random.randrange(Min,Max,1)
                for i in range(20):
                        if MillerRabin(p)==0:
                                break
                        elif i==19:
                                return p
                                
#加密，传入公钥，通过读取明文文件进行加密
def encrypt(m,e,n):
        cipher = ""
        nlength = len(str(hex(n))[2:])  #计算n的16进制长度，以便分组
        message = m             #读取明文
        for i in range(0,len(message),8):
            if i==len(message)//8*8:
                m = int(a2hex(message[i:]),16)  #最后一个分组
            m = int(a2hex(message[i:i+8]),16)
            c = MRF(m,e,n)
            cipher1 = str(hex(c))[2:]
            if len(cipher1)!=nlength:
                cipher1 = '0'*(nlength-len(cipher1))+cipher1    #每一个密文分组，长度不够，高位补0
            cipher += cipher1
        return cipher
#解密,传入私钥，通过文件读写进行解密
def decrypt(c,d,n):
        #加密之后每一个分组的长度和n的长度相同
        cipher = c
        message = ""
        nlength = len(str(hex(n))[2:])
        for i in range(0,len(cipher),nlength):
            c = int(cipher[i:i+nlength],16)     #得到一组密文的c
            m = MRF(c,d,n)
            info = hex2a(str(hex(m))[2:])
            message += info
        return message
 
#求最大公因子
def gcd(a,b):  
        if a%b == 0:
                return b
        else :
                return gcd(b,a%b)
 
#求逆元
def Ex_Euclid(x,n):
    r0=n
    r1=x%n
    if r1==1:
        y=1
    else:
        s0=1
        s1=0
        t0=0
        t1=1
        while (r0%r1!=0):
            q=r0//r1  
            r=r0%r1  
            r0=r1  
            r1=r  
            s=s0-q*s1 
            s0=s1 
            s1=s  
            t=t0-q*t1  
            t0=t1  
            t1=t  
            if r==1:
                y = (t+n)%n
    return y

 
#ascii_to_hex
def a2hex(raw_str):
        hex_str = ''
        for ch in raw_str:
                hex_str += hex(ord(ch))[2:]
        return hex_str
 
#hex_to_ascii
def hex2a(raw_str):
        asc_str = ''
        for i in range(0,len(raw_str),2):
                asc_str += chr(int(raw_str[i:i+2],16))
        return asc_str
def Build_key():
    #产生p,q,n,e,d
    p = BigPrime()
    q = BigPrime()
    n = p*q
    _n = (p-1)*(q-1)    #n的欧拉函数
    e = 0
    while(1):
            e = random.randint(1,_n+1)
            if gcd(e,_n)==1:
                    break
    d = Ex_Euclid(e,_n)
    return str(hex(n))[2:],str(hex(e))[2:],str(hex(d))[2:]

 
if __name__ == "__main__":
        main()