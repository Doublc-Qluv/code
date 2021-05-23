##判断是否与26互素
def isPN(a):
    for num in range(2,a):
        if 0==a%num and 0==26%num:
            return False
    return True

##求得逆元a_
def get_a_(a):
    i=1
    while (1!=(i*a)%26):
        i=i+1
    return i


##解密函数
def decodeMstr(mStr,a_,b):
    yStr=""
    for Char in mStr:
        if Char>='A' and Char<='Z':
            Int=ord(Char)-ord('A')
            Int=((Int-b+26)*a_)%26
            yStr=yStr+chr(Int+ord('A'))
        elif Char>='a' and Char<='z':
            Int=ord(Char)-ord('a')
            Int=((Int-b+26)*a_)%26
            yStr=yStr+chr(Int+ord('a'))
        else:
            yStr=yStr+Char
    return yStr

mStr="Ptfxgj Jnno-afv wn Htzaixojv Tjtxg"
for a in range(1,25,2):
    if False==isPN(a):
        continue
    else:
        a_=get_a_(a)
    for b in range(-10,10):
        yStr=decodeMstr(mStr,a_,b)
        print(yStr,end="\t")
        print(a,b)
