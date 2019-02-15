def fix():
    f=open('m0.txt','r')
    a=f.readline()
    a=a.strip()
    b=[a]        
    l=len(a)%16
    if l==0 :
        for i in range(16):
            b.append(chr(16))
    else :
        ll=16-l
        for i in range(ll):
            b.append(chr(ll)) 
    a=(''.join(b))
    print a
    f.close()
    f=open('m.txt','w')
    f.write(a)
    f.close()
#fix()

