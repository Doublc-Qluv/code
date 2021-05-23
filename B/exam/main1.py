import matplotlib.pyplot as plt
from TSP import TSP
from Map import Map
from dijkstra import Dijkstra_Path


#读取数据库中西电地图的内容
node_map,node=Map("./data.txt").data()
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


tsp=TSP(address=address_map,node=node,init_city=0,count=100)
gene=tsp.run(10000)

#起始站
begin=gene.index(0)
for i in range(begin,begin-len(gene),-1):
    print(node[gene[i]],"---->",end=' ')
print(node[gene[begin]])
