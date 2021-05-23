from Crypto.Random import random
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA
import hashlib
import math

#全局公共密钥
p =0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q =0xf4f47f05794b256174bba6e9b396a7707e563c5b
g =0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291
######################第一题########################
#用户公钥
y =0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17
#签名（r,s)
r = 548099063082341131477253921760299949438196259240
s = 857042759984254168557880549501802188789837994940
#收到消息的SHA1的值
M_SHA=0xd2d0714f014a9784047eaeccf956520045c45265
#密钥的SHA1的值
X_SHA=0x0954edd5e0afe5542a4adf012611a91912a3ec16
#######################第二题########################
#使用第一个和第三个来求解
s_2=[1267396447369736888040262262183731677867615804316,29097472083055673620219739525237952924429516683,277954141006005142760672187124679727147013405915,1013310051748123261520038320957902085950122277350,
203941148183364719753516612269608665183595279549,502033987625712840101435170279955665681605114553,1133410958677785175751131958546453870649059955513,559339368782867010304266546527989050544914568162,
1021643638653719618255840562522049391608552714967,506591325247687166499867321330657300306462367256,458429062067186207052865988429747640462282138703]
r_2=[1105520928110492191417703162650245113664610474875,51241962016175933742870323080382366896234169532,228998983350752111397582948403934722619745721541,1099349585689717635654222811555852075108857446485,
425320991325990345751346113277224109611205133736,486260321619055468276539425880393574698069264007,537050122560927032962561247064393639163940220795,826843595826780327326695197394862356805575316699,
1105520928110492191417703162650245113664610474875, 51241962016175933742870323080382366896234169532,228998983350752111397582948403934722619745721541]

m_2=[0xa4db3de27e2db3e5ef085ced2bced91b82e0df19,0xa4db3de27e2db3e5ef085ced2bced91b82e0df19,0x21194f72fe39a80c9c20689b8cf6ce9b0e7e52d4,0x1d7aaaa05d2dee2f7dabdc6fa70b6ddab9c051c5,
0x6bc188db6e9e6c7d796f7fdd7fa411776d7a9ff,0x5ff4d4e8be2f8aae8a5bfaabf7408bd7628f43c9,0x7d9abd18bbecdaa93650ecc4da1b9fcae911412,0x88b9e184393408b133efef59fcef85576d69e249,
0xd22804c4899b522b23eda34d2137cd8cc22b9ce8,0xbc7ec371d951977cba10381da08fe934dea80314,0xd6340bfcda59b6b75b59ca634813d572de800e8f]

#用户公钥y
y_2=0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821
X_SHA_2=0xca8f6f7c66fa362d40760d135b763eb8527d3d52

class modreverse(object):
    def __init__(self,a,m):
        self.a=a
        self.m=m

    def gcd(self,a,b):
        if a<b:
            a,b=b,a
        while b:
            a,b=b,a%b
        return a

    def fun(self):
        if self.gcd(self.a,self.m)!=1:
            return None
        u1,u2,u3=1,0,self.a
        v1,v2,v3=0,1,self.m
        while v3!=0:
            q=u3//v3
            v1,v2,v3,u1,u2,u3=(u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
        return u1%self.m


class crack(object):
    def __init__(self,p,q,g,y,r,s,M_SHA):
        self.p,self.q,self.g,self.y,self.r,self.s,self.M_SHA=p,q,g,y,r,s,M_SHA

    #低指数攻击
    def fun(self):
        for i in range(2**16):
            self.x_k_return=self.k_x(i,self.r,self.s,self.M_SHA)
            if self.x_k_return is not None:
                return self.x_k_return

    #共k攻击
    def fun2(self):
        for i in range(9):
            for j in range(i+1,11):
                rr=modreverse(self.s[i]-self.s[j],self.q).fun()
                if rr is not None:
                    k=(rr*(self.M_SHA[i]-self.M_SHA[j]))%q
                    self.x_k_return=self.k_x(k,self.r[i],self.s[i],self.M_SHA[i])
                    if self.x_k_return is not None:
                        print('msg%d'%(i+1),'and msg%d'%(j+1))
                        return self.x_k_return

    def k_x(self,k,r,s,M_SHA):
        if r==(pow(self.g,k,self.p)%self.q):
            print('k=',k)
            x=(((s*k)-M_SHA)*modreverse(r,self.q).fun())%self.q
            print('x=',x)
            x_sha1=hashlib.sha1(bytes(hex(x)[2:],encoding='utf-8')).hexdigest()
            print('x_sha1=',x_sha1)
            return x_sha1


"""
#根据模数求解
        #T=((self.g**u1)*(self.y**u2))%self.p        #???????????????
        #T=(((self.g**u1)%self.p)*((self.y**u2)%self.p))%self.p
        T=(pow(self.g,u1,self.p)*pow(self.y,u2,self.p))%self.p
"""
if __name__ == "__main__":
    #############################第一题##########################
    x_sha1=crack(p,q,g,y,r,s,M_SHA).fun()
    if eval('0x'+x_sha1)==X_SHA:
        print('第一题：成功,得到的私钥SHA1与已知私钥的SHA1相同。')
    #############################第二题##########################
    x_sha1_2=crack(p,q,g,y_2,r_2,s_2,m_2).fun2()
    if eval('0x'+x_sha1_2)==X_SHA_2:
        print('第二题：成功,得到的私钥SHA2与已知私钥的SHA2相同。')