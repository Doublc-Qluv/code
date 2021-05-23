import numpy as np
import random

#读入数据
def readfile():
    global alldata,M,R
    read=open('sonar.all-data')
    data=[1]*(alldata.shape[1]-1)
    while True:
        s=read.readline()
        s=s.split(',')
        if len(s) == 1:
            break
        data[0]=float(s[0])
        for i in range(0,alldata.shape[1]-1):
            data[i]=float(s[i])
        if s[60]=='R\n':
            R=np.row_stack((R, data))
        if s[60]=='M\n':
            M=np.row_stack((M, data))
        alldata=np.row_stack((alldata, s))
    read.close()

#返回该DNA链的基于类内类间距离的类别可分性判据
def getf(l):
    #生成特征向量
    Xm=np.zeros(shape=(0,D))
    Xr=np.zeros(shape=(0,D))
    Mr=[0]*D
    Mm=[0]*D
    for i in range(0,Nr):
        temp=[]
        for j in range (0,L_LENGTH):
            if l[j]==1:
                temp.append(R[i][j])
        Xr=np.row_stack((Xr,temp))
        Mr=np.add(Mr,temp)
    for i in range(0,Nm):
        temp=[]
        for j in range (0,L_LENGTH):
            if l[j]==1:
                temp.append(M[i][j])
        Xm=np.row_stack((Xm,temp))
        Mm=np.add(Mm,temp)
    #计算类别可分性判别函数
    Mr=np.multiply(1/Nr,Mr)
    Mm=np.multiply(1/Nm,Mm)
    Mall=np.multiply(Pr,Mr)+np.multiply(Pm,Mm)
    Sb=np.multiply(Pr,np.dot(np.mat(Mr-Mall),np.mat(Mr-Mall).T))+np.multiply(Pm,np.dot(np.mat(Mm-Mall),np.mat(Mm-Mall).T))
    Sr=np.zeros(shape=(D,D))
    Sm=np.zeros(shape=(D,D))
    for i in range(0,Nr):
        Sr=Sr+np.dot(np.mat(Xr[i]-Mr),np.mat(Xr[i]-Mr).T)
    Sr=np.multiply(1/N,Sr)
    for i in range(0, Nm):
        Sm=Sm+np.dot(np.mat(Xm[i]-Mm),np.mat(Xm[i]-Mm).T)
    Sm=np.multiply(1/N,Sm)
    Sw=Sr+Sm
    return np.trace(np.mat(Sb+Sw))

#产生新的染色体
def born(l1,l2):
    pb=random.random()
    #突变过程
    if(pb<pm):
        i=random.randint(0,L_LENGTH-1)
        j=i
        while(l1[j]==l1[i]):
            j=random.randint(0,L_LENGTH-1)
        l1[i]=l1[i]^1
        l1[j]=l1[j]^1
        i=random.randint(0, L_LENGTH-1)
        j=i
        while (l2[j]==l2[i]):
            j=random.randint(0, L_LENGTH-1)
        l2[i]=l2[i]^1
        l2[j]=l2[j]^1
    if(pb>pc):
        return l1,l2
    #重组过程
    else:
        double_1=0
        singl_0=[-1]*L_LENGTH
        singl_1=[-1]*L_LENGTH
        for i in range (0,L_LENGTH):
            if l1[i]==1 and l2[i]==1:
                double_1=double_1+1
            elif l1[i]==0 and l2[i]==1:
                singl_0[i]=i
            elif l1[i]==1 and l2[i]==0:
                singl_1[i]=i
        exchange_1=random.randint(0,(D-double_1))
        cot=0
        for i in range(0,L_LENGTH):
            if singl_0[i]!=-1:
                l1[i]=1
                l2[i]=0
                cot=cot+1
                if cot==exchange_1:
                    break
        cot=0
        for i in range(L_LENGTH-1,-1,-1):
            if singl_1[i]!=-1:
                l1[i]=0
                l2[i]=1
                cot=cot+1
                if cot==exchange_1:
                    break
        return l1,l2

#GA
#读入数据与初始化变量
alldata=np.zeros(shape=(0, 61))  #全体数据带标签
R=np.zeros(shape=(0,60))    #R
M=np.zeros(shape=(0,60))    #M
readfile()
M_SIZE=500   #种群容量
L_LENGTH=alldata.shape[1]-1 #染色体长度
D=20        #提取的特征数目
pc=0.6      #重组概率
pm=1.005    #突变概率
T=30   #迭代次数
N=alldata.shape[0]  #全体样本个数
Nr=R.shape[0]   #R样本个数
Nm=M.shape[0]   #M样本个数
Pr=Nr/N #R先验概率
Pm=Nm/N #M先验概率
ansf=0
ansl=[]
F=[]

#随机产生初始种群
m=[]
for i in range(0,M_SIZE):
    #随机产生一条染色体
    l=[0]*L_LENGTH
    cot=0;
    while cot<D:
        index=random.randint(0,L_LENGTH-1)
        if l[index]==0:
            l[index]=1
            cot=cot+1
    m.append(l)

t=0
while t<T:
    t=t+1
    #print("The %d-th generation:"%(t))
    #计算当前种群每一条染色体的种群适应度并得到最大的适应度
    f=[0]*M_SIZE
    sumf=0
    maxf=-1
    maxi=-1
    for i in range(0,M_SIZE):
        f[i]=getf(m[i])
        sumf=sumf+f[i]
        if f[i]>maxf:
            maxf=f[i]
            maxi=i
            if (maxf>ansf):
                ansf=maxf
                ansl=m[i]
    print("%f,%f" % (maxf, sumf / M_SIZE))
    F.append(sumf / M_SIZE)

    #计算当前种群每一条染色体的选择概率及概率轮盘
    max=0
    min=10
    p=[0]*M_SIZE
    for i in range(0,M_SIZE):
        p[i]=f[i]/sumf
        if p[i]>max:
            max=p[i]
        if p[i]<min:
            min=p[i]
    wheel=[0]*(M_SIZE+1)
    for i in range(1,M_SIZE+1):
        wheel[i]=wheel[i-1]+p[i-1]
    #print(max)
    #print(min)

    #产生新的种群
    newm=[0]*M_SIZE
    i=0;
    while i<M_SIZE:
        #按照p(f(l))对种群中的染色体进行采样
        temp=random.random()
        for j1 in range(1,M_SIZE+1):
            if temp>wheel[j1-1] and temp<=wheel[j1]:
                break
        temp=random.random()
        for j2 in range(1,M_SIZE+1):
            if temp>wheel[j2-1] and temp<=wheel[j2]:
                break
        #繁殖下一代
        newl1,newl2=born(m[j1-1],m[j2-1])
        newm[i]=newl1
        i=i+1
        newm[i]=newl2
        i=i+1
    m=newm

print("The result of selection:",ansl)