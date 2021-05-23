import matplotlib.pyplot as plt
from TSP import TSP
from Map import Map
from dijkstra import Dijkstra_Path

import random

#读取数据库中西电地图的内容
(node_map,node,weight)=Map("data.txt").data()
print(node_map,node)

#迪杰斯特拉算法求解对应点之间的最短距离
for i in range(len(node)):
    for j in range(len(node)):
        if i!=j and node_map[i][j]==0:
            node_map[i][j]=9999

address_map=[]
Dijkstra=Dijkstra_Path(node_map)
for i in range(len(node)):
    address_map.append(Dijkstra(i,i-1))
"""

print(address_map)


#输出遍历顺序
def print_seq(address_map,node):
    tsp=TSP(address=address_map,node=node,init_city=0,count=100)
    gene=tsp.run(10000)
    begin=gene.index(0)     #起始站位置
    for i in range(begin,begin-len(gene),-1):
        print(node[gene[i]],"---->",end=' ')
    print(node[gene[begin]])
"""


#输出遍历顺序
def print_seq(address_map,node0,node):
    tsp=TSP(address=address_map,node=node0,init_city=0,count=300)
    gene=tsp.run(10000)
    begin=gene.index(0)     #起始站位置
    for i in range(begin,begin-len(gene),-1):
        print(node[gene[i]],"---->",end=' ')
    print(node[gene[begin]])


for i in range(1000):
    print(i)
    sum=0
    for i in weight:
        sum+=i
    weight1=[]
    node00=[]
    for i in range(len(weight)):
        weight1.append(weight[i]/sum)
        node00.extend([node[i]]*int(weight1[i]*100))
    node0=random.sample(node00,20)
    node000=[]
    for i in node0:
        if i not in node000:
            node000.append(i)
    address0=[]
    for i in node000:
        address=[]
        for j in node000:
            address.append(address_map[node.index(i)][node.index(j)])
        address0.append(address)
    print_seq(address0,node000,node)



"""
#一条线路
#print_seq(address_map,node)
#两条线路
node1=node[:14]
node2=node[8:]
node2.insert(0,"东门")
address1=[]
address2=[]
for i in node1:
    address=[]
    for j in node1:
        address.append(address_map[node.index(i)][node.index(j)])
    address1.append(address)
for i in node2:
    address=[]
    for j in node2:
        address.append(address_map[node.index(i)][node.index(j)])
    address2.append(address)


#print_seq(address1,node1)
#print_seq(address2,node2)

node3=["东门","南操","A楼","D楼","B楼","大活","丁香","家属区"]
node4=["东门","北操","信远","海棠","竹园","A楼","D楼","B楼","新综","老综"]
address3=[]
address4=[]
for i in node3:
    address=[]
    for j in node3:
        address.append(address_map[node.index(i)][node.index(j)])
    address3.append(address)
for i in node4:
    address=[]
    for j in node4:
        address.append(address_map[node.index(i)][node.index(j)])
    address4.append(address)


print_seq(address3,node3)
print_seq(address4,node4)

"""