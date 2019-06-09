INF_val = 9999  


class Dijkstra_Path():  
    def __init__(self, node_map):  
        self.node_map = node_map  
        self.node_length = len(node_map)  
      
    def __call__(self, from_node, to_node):  
        self.from_node = from_node  
        self.to_node = to_node  
        self.path=[-1]*self.node_length
        self.to_node_path=[]
        self.s=[True]*self.node_length
        return self._init_dijkstra()  
  
    def _init_dijkstra(self):
        self.dist=self.node_map[self.from_node]
        for i,m in enumerate(self.dist):
            if i!=self.from_node:
                self.s[i]=False
                self.path[i]=self.from_node
        self.to_node_path.append(self.path[self.to_node])
        while True:
            try:
                self.s.index(False)
            except:
                return self.dist
            else:
                self.grade()
        
        
        

    def grade(self):
        #查找最小值
        self.min=INF_val
        self.min_index=0
        for i,m in enumerate(self.s):
            if m!=True:
                if self.min>self.dist[i]:
                    self.min=self.dist[i]
                    self.min_index=i
        self.s[self.min_index]=True
        self.temp=self.node_map[self.min_index]
        for i in range(len(self.dist)):
            if self.temp[i]+self.min<self.dist[i]:
                self.dist[i]=self.temp[i]+self.min
                self.path[i]=self.min_index
                if i==self.to_node:
                    self.to_node_path.append(self.min_index)
