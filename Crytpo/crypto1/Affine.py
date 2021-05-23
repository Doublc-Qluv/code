#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# E(x) = (ax+b) mod m
# D(x) = (a^-1)(x-b) mod m

# 判断是否互素 即判断a和m是否互素，
def gcd(a,b):
    while a!=0:
        a,b = b%a,a
    return b

def findModReverse(a,m):#这个扩展欧几里得算法求模逆，辗转相除法

    if gcd(a,m)!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1
m = 26
a = int(input())

def encryption(plaintext):# 加密算法
    cipherarr = [0 for i in range(len(plaintext))]
    plaintext_list = list(plaintext)

    j = 0
    for plaintext_item in plaintext_list:
        for i in range(len(plaintext)):
            if plaintext_item == plaintext[i]:
                ciphertext = (11*i+4)%26
                cipherarr[j] = ciphertext[ciphertext]
                j = j+1

    cipher = ''.join(cipherarr)
    return cipher

findModReverse(a,m)
print(findModReverse(a,m))