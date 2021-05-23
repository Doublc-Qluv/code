import numpy as np
from math import gcd

#求解行列式函数
def det(m):
    if len(m) <= 0:
        return None
    elif len(m) == 1:
        return m[0][0]
    else:
        s = 0
        for i in range(len(m)):
            n = [[row[a] for a in range(len(m)) if a != i] for row in m[1:]] # 这里生成余子式
            s += m[0][i] * det(n) * (-1) ** (i % 2)
        return s



#产生秘钥
def kyeproduc(N):
    while 1:
        key1=np.random.randint(0,25,size=(N,N))
        key2=np.random.randint(0,25,size=(N,1))
        val=det(key1)%26
        if 1==gcd(val,26) and val!=0:  #可逆的条件
            break
    key_1=inver(key1,N)
    key=[key1,key_1,key2]
    return key

#求模逆矩阵---使用伴随矩阵乘以行列式(模26前提下)
def inver(key,N):
    val=det(key)%26
    adjoint=np.random.randint(1,10,size=(N,N))
    for val_1 in range(26):  #伴随矩阵求逆矩阵需要除以行列式，为保证逆矩阵元素为整数，求行列式模26的逆
        if val_1*val%26==1:
            break
    for i in range(N):
        for j in range(N):
            adjoint[i][j]=follow(key,i,j,N)%26
    inv=(adjoint*val_1)%26
    return inv


def follow(key,i,j,N):
    key1=[]
    c,l=key.shape[0],key.shape[1]
    for m in range(c):
        for n in range(l):
            if m!=i and n!=j:
                key1.append(key[n,m])
    key1=np.array(key1).reshape(N-1,N-1)
    t=(-1)**(i+j)*det(key1)
    return t

#明文变为矩阵
def textproduc(text,N):
    textarray=[]
    t=0
    for i in text:
        if ord(i)>=ord('A') and ord(i)<=ord('Z'):
            textarray.append(ord(i))
        else:
            textarray.append(ord(i)-32)
    length=len(textarray)
    #分组不够的地方补充A
    if length%N:
        while 1:
            textarray.append(ord('A'))
            t+=1
            if(0==(t+length)%N):
                break
    textarray2=np.array(textarray)
    textarray3 = np.transpose(textarray2.reshape(-1,N))-65  #将信息转化为k例矩阵
    return textarray3

#enceyption(text,randarray)--->使用两个秘钥对信息矩阵进行加密
def encryption(text,randarray):
    text=(np.dot(randarray[0],text)+randarray[2])%26 #加密部分
    return text

#decryption(text,randarray)--->使用两个秘钥对加密矩阵进行解密
def decryption(text,randarray):
    text=np.dot(randarray[1],text-randarray[2])%26
    return text

#textproduc2(text)--->将矩阵转化为字符串
def textproduc2(text):
    text = np.transpose(text)
    message=[]
    c, l = text.shape[0], text.shape[1]
    for i in range(c):
        for j in range(l):
            message.append(chr(text[i, j]%26+97))
    message2=''.join(message)
    return message2

if __name__ == '__main__':
    N=3
    keyarray=kyeproduc(N)
    text=input("enter your text:")
    message=textproduc(text,N)
    enmessage=encryption(message,keyarray)
    enmessage=textproduc2(enmessage)
    print('ciphertext:',enmessage)
    demessaage=textproduc(enmessage,N)
    print('dephertext:',textproduc2(decryption(demessaage,keyarray)))