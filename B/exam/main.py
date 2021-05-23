import matplotlib.pyplot as plt
from TSP import TSP
from read_data import read_data

import tkinter as tk
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体

City=read_data("data.txt").data()


for i,c in enumerate(City):
    print("%d:%s"%(i,c[0]))

a=input("请输入城市：")
a=a.split()
aa=[]
for i in a:
    aa.append(City[int(i)])
print(aa)
tsp=TSP(city=aa,init_city=0,count=100)
gene=tsp.run(3000)
print(gene)
city_x=[]
city_y=[]


plt.figure(2)
for i in range(-1,len(gene),1):
    plt.scatter(aa[i][1],aa[i][2],color='r')
    plt.text(aa[i][1],aa[i][2]+0.2,aa[i][0])
    city_x.append(aa[i][1])
    city_y.append(aa[i][2])
plt.plot(city_x,city_y,color='b',linewidth=0.5)

plt.show()