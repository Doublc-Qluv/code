class creategcd(object):
    def __init__(self, key1,mod):
        self.a = key1
        self.b = mod
        self.m = mod

    def gcd(self,a,b):
        while self.a!=0:
            self.a,self.b = self.b%self.a,self.a
        return self.b

    def findModReverse(self,a,m):#这个扩展欧几里得算法求模逆，辗转相除法

        if self.gcd(self.a,self.b)!=1:
            return None
        self.u1,self.u2,self.u3 = 1,0,self.a
        self.v1,self.v2,self.v3 = 0,1,self.m
        while self.v3!=0:
            self.q = self.u3//self.v3
            self.v1,self.v2,self.v3,self.u1,self.u2,self.u3 = (self.u1-self.q*self.v1),(self.u2-self.q*self.v2),(self.u3-self.q*self.v3),self.v1,self.v2,self.v3
        return self.u1
    def cprint(self):
        print(self.findModReverse)


if __name__ == "__main__":
    a = int(input())
    b = creategcd(a,26)
    b.cprint