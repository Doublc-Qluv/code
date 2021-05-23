import hashlib
import base64
import binascii
import binhex
import math

#SBOX
SBOX_table=[
    'd6', '90', 'e9', 'fe', 'cc', 'e1', '3d', 'b7', '16', 'b6', '14', 'c2', '28', 'fb', '2c', '05',
    '2b', '67', '9a', '76', '2a', 'be', '04', 'c3', 'aa', '44', '13', '26', '49', '86', '06', '99',
    '9c', '42', '50', 'f4', '91', 'ef', '98', '7a', '33', '54', '0b', '43', 'ed', 'cf', 'ac', '62',
    'e4', 'b3', '1c', 'a9', 'c9', '08', 'e8', '95', '80', 'df', '94', 'fa', '75', '8f', '3f', 'a6',
    '47', '07', 'a7', 'fc', 'f3', '73', '17', 'ba', '83', '59', '3c', '19', 'e6', '85', '4f', 'a8',
    '68', '6b', '81', 'b2', '71', '64', 'da', '8b', 'f8', 'eb', '0f', '4b', '70', '56', '9d', '35', 
    '1e', '24', '0e', '5e', '63', '58', 'd1', 'a2', '25', '22', '7c', '3b', '01', '21', '78', '87', 
    'd4', '00', '46', '57', '9f', 'd3', '27', '52', '4c', '36', '02', 'e7', 'a0', 'c4', 'c8', '9e', 
    'ea', 'bf', '8a', 'd2', '40', 'c7', '38', 'b5', 'a3', 'f7', 'f2', 'ce', 'f9', '61', '15', 'a1',
    'e0', 'ae', '5d', 'a4', '9b', '34', '1a', '55', 'ad', '93', '32', '30', 'f5', '8c', 'b1', 'e3',
    '1d', 'f6', 'e2', '2e', '82', '66', 'ca', '60', 'c0', '29', '23', 'ab', '0d', '53', '4e', '6f',
    'd5', 'db', '37', '45', 'de', 'fd', '8e', '2f', '03', 'ff', '6a', '72', '6d', '6c', '5b', '51',
    '8d', '1b', 'af', '92', 'bb', 'dd', 'bc', '7f', '11', 'd9', '5c', '41', '1f', '10', '5a', 'd8',
    '0a', 'c1', '31', '88', 'a5', 'cd', '7b', 'bd', '2d', '74', 'd0', '12', 'b8', 'e5', 'b4', 'b0',
    '89', '69', '97', '4a', '0c', '96', '77', '7e', '65', 'b9', 'f1', '09', 'c5', '6e', 'c6', '84',
    '18', 'f0', '7d', 'ec', '3a', 'dc', '4d', '20', '79', 'ee', '5f', '3e', 'd7', 'cb', '39', '48'
]
#系统参数
CK= [
    0x00070e15,0x1c232a31,0x383f464d,0x545b6269,
    0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,
    0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,
    0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,
    0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,
    0x30373e45,0x4c535a61,0x686f767d,0x848b9299,
    0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,
    0x10171e25,0x2c333a41,0x484f565d,0x646b7279
]
#固定参数
FK=[0xa3b1bac6,0x56aa3350,0x677d9197,0xb27022dc]
#加密密钥--128比特
#MK=bitarray(128)
key=b'0123456789ABCDEFFEDCBA9876543210'
MK=[]
#明文
TEXT=b'0123456789ABCDEFFEDCBA9876543210'
"""
a=iter(key)
MK=[]
c=''
for i in range(16):
    if i%4==0:
        MK.append(c)
        print(c)
        c=''
    c=c+hex(a.__next__())[2:4]
    print(hex(a.__next__())[2:4])
"""
for i in range(4):
    MK.append(eval(b'0x'+key[4*i:4*i+4]))



#PKCS#7填充
class PKCS(object):
    def __init__(self,text):
        self.text=text
        self.context=[]
        self.fun()

    #填充
    def fun(self):
        text_len=len(self.text)
        if text_len%16:
            self.text=self.text+(16-text_len%16)*chr(16-text_len%16)
        for i in range(4*(math.ceil(text_len/16))):
            self.context.append(eval(b'0x'+binascii.b2a_hex(bytes(self.text[4*i:4*i+4],encoding='utf-8'))))
#轮密钥
rk=[]



#轮密钥的计算------密钥拓展算法
class key_extension(object):
    def __init__(self,FK,CK,MK):
        #FK为系统参数,CK为固定参数,MK为加密密钥
        self.fk=FK
        self.ck=CK
        self.mk=MK
        self.k=[]
        self.rk=[]
        self.fun()
    
    #轮密钥线性变换
    def linear_round(self,b):
        c=eval(b)^shift(b,13).fun()^shift(b,23).fun()
        return c

    #非线性变换
    def not_linear(self,x1,x2,x3,rk1):
        a='0x'+hex(x1^x2^x3^rk1)[2:].zfill(8)
        b=''
        for i in range(2,10,2):
            b=b+SBOX_table[int(a[i:i+2],16)]
        b='0x'+b.zfill(8)
        return b

    def fun(self):
        for i in range(4):
            self.k.append(self.mk[i]^self.fk[i])
        #合成置换
        for j in range(32):
            t=self.linear_round(self.not_linear(self.k[j+1],self.k[j+2],self.k[j+3],self.ck[j]))
            rk=self.k[j]^t
            self.k.append(rk)
            self.rk.append(rk)
            #print(hex(rk))

#循环左移运算
class shift(object):
    def __init__(self,lst,n):
        self.lst=lst
        self.n=n

    def fun(self):
        self.bin_lat=bin(eval(self.lst))
        self.bin_lat='0b'+self.bin_lat[2:].zfill(32)                #转换为二进制时，前面的0省去了
        return eval('0b'+self.bin_lat[self.n+2:]+self.bin_lat[2:self.n+2])    

#轮函数F
class F(key_extension):
    def __init__(self,rkn,x0,x1,x2,x3):
        self.rkn=rkn
        self.x0=x0
        self.x1=x1
        self.x2=x2
        self.x3=x3
        self.y=self.fun()
    
    #线性变换
    def linear_F(self,b):
        c=eval(b)^shift(b,2).fun()^shift(b,10).fun()^shift(b,18).fun()^shift(b,24).fun()
        return c
    
    def fun(self):
        #合成置换
        t=self.linear_F(self.not_linear(self.x1,self.x2,self.x3,self.rkn))
        f=self.x0^t
        return f

#加密算法
class encry(object):
    def __init__(self,X,RK):
        #要加密的明文X，轮密钥RK
        self.x=X
        self.rk=RK
        self.y=[]
        self.reverse()

    #32次迭代运算
    def iteration(self):
        for i in range(32):
            self.x.append(F(self.rk[i],self.x[i],self.x[i+1],self.x[i+2],self.x[i+3]).y)

    #反序变换
    def reverse(self):
        #调用32次迭代运算，然后反序变换
        self.iteration()
        for i in range(4):
            self.y.append(self.x[-(i+1)])
        #for i in range(len(self.x)):
            #print('x%d'%i,hex(self.x[i]))

class decry(object):
    def __init__(self,Y,RK):
        #要解密的密文Y，轮密钥RK
        self.y=Y
        self.rk=RK
        self.x=[]
        self.reverse()
    
    #此处与加密算法不同
    def iteration(self):
        for i in range(32):
            self.y.append(F(self.rk[-(i+1)],self.y[i],self.y[i+1],self.y[i+2],self.y[i+3]).y)
    
    #反序变换
    def reverse(self):
        #调用32次迭代运算，然后反序变换
        self.iteration()
        for i in range(4):
            self.x.append(self.y[-(i+1)])

if __name__ == "__main__":
    while(True):
        print('       SM4加解密\n1.加密\n2.解密\n3.退出\n')
        q=input('你要进行的操作：')
        if q=='1' or q=='2':
            MK=[]
            while True:
                key=input('请输入密钥（16个字符）：')
                if len(key)==16:
                    break
            key=bytes(key,encoding='utf-8')
            for i in range(4):
                MK.append(eval(b'0x'+key[4*i:4*i+4]))
            RK=key_extension(FK,CK,MK).rk    #计算轮密钥，RK是计算出来的轮密钥，FK是系统参数，CK是固定参数，MK是加密密钥
            if q=='1':
                TEXT=input('请输入你要加密的东西')
                text=PKCS(TEXT).context          #明文填充,text是填充后的结果
                Y=encry(text,RK).y                    #加密算法,Y是加密后的结果
                aa=''
                for i in range(len(Y)):
                    for j in range(1,5):
                        aa=aa+chr(eval('0x'+(hex(Y[i]).zfill(8)[2*j:2*j+2])))
                print('加密结果：',aa)
            if q=='2':
                while True:
                    TEXT=input('请输入你要解密的东西')
                    if len(TEXT)%16==0:
                        text=PKCS(TEXT).context
                        break
                decry_text=decry(text,RK).x
                aa=''
                for i in range(len(decry_text)):
                    for j in range(1,5):
                        aa=aa+chr(eval('0x'+(hex(decry_text[i]).zfill(8)[2*j:2*j+2])))
                print('解密结果：',aa)
        elif q=='3':
            break

"""
    RK=key_extension(FK,CK,MK).rk    #计算轮密钥，RK是计算出来的轮密钥，FK是系统参数，CK是固定参数，MK是加密密钥
    text=PKCS(TEXT).context          #明文填充,text是填充后的结果
    Y=encry(text,RK).y                    #加密算法,Y是加密后的结果
    for i in range(4):
        print(hex(Y[i]))
    decry_text=decry(Y,RK).x
    for i in range(4):
        print(hex(decry_text[i]))"""