import hashlib
import base64
import binascii
import binhex
import time


#初始置换表
initial_table=[
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7,
]

#逆初始置换
inverse_initial_table=[
    40, 8,	48,	16,	56,	24,	64,	32,
    39,	7,	47,	15,	55,	23,	63,	31,
    38,	6,	46,	14,	54,	22,	62,	30,
    37,	5,	45,	13,	53,	21,	61,	29,
    36,	4,	44,	12,	52,	20,	60,	28,
    35,	3,	43,	11,	51,	19,	59,	27,
    34,	2,	42,	10,	50,	18,	58,	26,
    33,	1,	41,	9,	49,	17,	57,	25,
]
#扩张函数（E函数）
expansion_fun_table=[
    32,	1,	2,	3,	4,	5,
    4,	5,	6,	7,	8,	9,
    8,	9,	10,	11,	12,	13,
    12,	13,	14,	15,	16,	17,
    16,	17,	18,	19,	20,	21,
    20,	21,	22,	23,	24,	25,
    24,	25,	26,	27,	28,	29,
    28,	29,	30,	31,	32,	1,
]
#p置换
P_replament=[
    16,	7,	20,	21,
    29,	12,	28,	17,
    1,	15,	23,	26,
    5,	18,	31,	10,
    2,	8,	24,	14,
    32,	27,	3,	9,
    19,	13,	30,	6,
    22,	11,	4,	25,
]

#选择置换1（PC-1)
PC_1=[
    57,	49,	41,	33,	25,	17,	9,
    1,	58,	50,	42,	34,	26,	18,
    10,	2,	59,	51,	43,	35,	27,
    19,	11,	3,	60,	52,	44,	36,
    63,	55,	47,	39,	31,	23,	15,
    7,	62,	54,	46,	38,	30,	22,
    14,	6,	61,	53,	45,	37,	29,
    21,	13,	5,	28,	20,	12,	4
]
#选择置换2（PC-2）
PC_2=[
    14,	17,	11,	24,	1,	5,
    3,	28,	15,	6,	21,	10,
    23,	19,	12,	4,	26,	8,
    16,	7,	27,	20,	13,	2,
    41,	52,	31,	37,	47,	55,
    30,	40,	51,	45,	33,	48,
    44,	49,	39,	56,	34,	53,
    46,	42,	50,	36,	29,	32
]
#密钥调度过程中的移位
shift_table=[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

#置换盒（s盒）
S_table=[
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
    0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
    4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
    15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
    3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
    0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
    13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
    13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
    13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
    1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5 ,11, 12, 4, 15,
    13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
    10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
    3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
    14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
    4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
    11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
    10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
    9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
    4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
    13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
    1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
    6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
    1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
    7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
    2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]



class key(object):
    def __init__(self,mk):
        #mk加密的密钥（64比特）
        self.mk=bin(eval('0x'+mk))[2:].zfill(64)
        #print(self.mk)
        self.k=[]
        self.fun()

    #主函数
    def fun(self):
        self.replace1()
        for i in range(16):
            self.C.append(self.shift(self.C[i],i))
            self.D.append(self.shift(self.D[i],i))
            print('c%d:'%(i+1),self.C[i+1],'d%d:'%(i+1),self.D[i+1])
            self.k.append(self.replace2(self.C[i+1]+self.D[i+1]))
    
    #置换选择运算1
    def replace1(self):
        #置换运算
        lst=''
        for i in range(56):
            lst=lst+self.mk[PC_1[i]-1]       
        #分割
        self.C=[lst[:28]]
        self.D=[lst[28:]]
        #print(lst[:28],lst[28:])

    #置换选择2
    def replace2(self,lst):
        lst2=''
        for i in range(48):
            lst2=lst2+lst[PC_2[i]-1]    
        return lst2

    #循环移位操作
    def shift(self,lst,n):
        a=shift_table[n]
        return lst[a:]+lst[:a]


#加密算法
class encry(object):
    def __init__(self,mk,data):
        #mk加密的子密钥（16个），data是要加密的明文（64比特）
        self.mk=mk
        self.data=data

    def fun(self):
        self.initial_IP()                                       #初始置换IP运算
        self.wheel=wheel_stucture(self.mk,self.initial_data)    #轮结构加密
        self.L=self.wheel.L
        self.R=self.wheel.R
        #轮结构加密后的结果
        for i in range(17):
            print('L%d:'%(i),self.L[i])
            print('R%d:'%(i),self.R[i])
        #左右交换
        self.E=self.R[4]+self.L[4]
        print('左右交换后的结果：\n',self.E)
        #逆初始转换
        content='0b'
        for i in range(64):
            content=content+self.E[inverse_initial_table[i]-1]
        print('逆初始转换后的结果：\n',content)
        #加密结果
        self.text=hex(eval(content))
        print('加密后的结果：\n',self.text)      

    #初始置换IP
    def initial_IP(self):
        self.initial_data='0b'
        self.bin_data=bin(eval('0x'+self.data))[2:].zfill(64)
        for i in range(64):
            self.initial_data=self.initial_data+self.bin_data[initial_table[i]-1]
        print('经过初始置换IP后的结果：\n',self.initial_data[2:])

class decry(encry):
    def __init__(self,mk,data):
        encry.__init__(self,mk,data)
    def fun(self):
        self.initial_IP()                                       #初始置换IP运算
        self.wheel=wheel_stucture(self.mk,self.initial_data)    #轮结构加密
        self.L=self.wheel.L
        self.R=self.wheel.R
        #左右交换
        self.E=self.R[4]+self.L[4]
        #逆初始转换
        content='0b'
        for i in range(64):
            content=content+self.E[inverse_initial_table[i]-1]
        #解密结果
        self.text=hex(eval(content))
        print('解密密后的结果：\n',self.text)   

#轮
class wheel_stucture(object):
    def __init__(self,k,data):
        #k是置换选择后的16个加密密钥（48比特），data是经过初始置换要加密的密文（64比特）
        self.k=k
        self.data=data
        self.L=[self.data[2:34]]   
        self.R=[self.data[34:66]]
        self.Feistel()

    #Feistel网络函数
    def Feistel(self):
        for i in range(16):
            self.L.append(self.R[i])
            self.F(self.R[i],self.k[i])
            self.R.append(bin(eval('0b'+self.L[i])^eval(self.p_data))[2:].zfill(32))

    #Feistel网络的算法
    def F(self,r,k):
        #扩展
        self.expension_data='0b'
        for i in range(48):
            self.expension_data=self.expension_data+r[expansion_fun_table[i]-1]
        k='0b'+k
        #异或运算
        self.s_data='0b'+bin(eval(k)^eval(self.expension_data))[2:].zfill(48)
        self.S()   #S盒
        #P置换
        self.p_data='0b'
        for i in range(32):
            self.p_data=self.p_data+self.p[P_replament[i]-1]

    #S盒
    def S(self):
        #分割
        self.s=[]    #分割成八分
        self.p=''    #S和置换后
        for i  in range(2,50,6):
            self.s.append(self.s_data[i:i+6])
        for i in range(8):
            self.p=self.p+bin(S_table[i][eval('0b'+self.s[i][0]+self.s[i][5]+self.s[i][1:5])])[2:].zfill(4)


if __name__ == "__main__":
    K='133457799BBCDFF1'     #密钥
    start = time.clock()
    encry_key=key(K).k       #子密钥的生成，encry_key为子密钥

    M='0123456789ABCDEF'     #明文
    for i in range(16):              #输出密钥
        print('K%d:'%(i+1),encry_key[i])
    print('明文M:',M,'\n明文的二进制：\n',bin(eval('0x'+M))[2:].zfill(64))     #输出明文
    
    encry(encry_key,M).fun()    #加密
    
    end1 = time.clock()
    print("加密用时："+str(end1-start))