#*- coding:utf-8 -*#
import numpy

weigh_graph = [[10000, 2, 4, 5],
                 [2,10000, 7, 8],
                 [4, 7, 10000, 4],
                 [5, 8, 4,10000]]
# weigh_graph = numpy.array(a + numpy.transpose(a))
source_node = 0
target_node = 3

vertices=set(range(len(weigh_graph)))

path=[]
for j in vertices:
  path.append(0 if j==source_node else float("inf"))

current_node=source_node
visited_node=[]
unvisited_node=vertices
orders=[source_node]

while target_node in unvisited_node:

    for j in unvisited_node:
        if path[j] < path[current_node]+weigh_graph[current_node][j]:
             path[j] =path[j]
        else:
             path[j] = path[current_node]+weigh_graph[current_node][j]

    unvisited_node.discard(current_node)
    print(unvisited_node)

    for index,value in enumerate(weigh_graph[current_node]):
        if index in unvisited_node:
            if value==min(weigh_graph[current_node][j] for j in unvisited_node):
                 print(min(weigh_graph[current_node][j] for j in unvisited_node))
                 current_node = index

    # current_node=list(weigh_graph[current_node]).index(min(weigh_graph[current_node][j] for j in unvisited_node))
    #这样找索引会出现索引第一个的情况，但是需要确定所引导的位置并没有被作为顶点

    print(current_node)
    orders.append(current_node)
    if current_node==target_node:
        break

print(orders)
print(path)
