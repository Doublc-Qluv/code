import numpy as np 

class Map():
    def __init__(self,PATH):
        self.path=PATH

    def data(self):
        try:
            #读取文件
            with open(self.path,'r') as FILE:
                address=[]
                node=FILE.readline().replace('\n','').split(' ')
                for i in FILE.readlines():
                    add=i.split(' ')
                    #address.append([add[0],np.array([float(add[1]),float(add[2])])])
                    address.append((add[0],add[1],float(add[2])))
            #构建图 
            node_map = [[0 for val in range(len(node))] for val in range(len(node))] 
            for x, y, val in address:  
                node_map[node.index(x)][node.index(y)] = node_map[node.index(y)][node.index(x)] = val  
            return node_map,node
        except:
            return 'read file error'
