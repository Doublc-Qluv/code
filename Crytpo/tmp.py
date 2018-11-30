def gcd(a,b):
    while a!=0:
        a,b = b%a,a
    return b
#定义一个函数，参数分别为a,n，返回值为b
def findModReverse(a,m):#这个扩展欧几里得算法求模逆

    if gcd(a,m)!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1
a,m = input().split()
findModReverse(a,m)
print(findModReverse(a,m))