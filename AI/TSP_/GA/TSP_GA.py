# -*- encoding: utf-8 -*-
 
import random
import math
import sys
import tkinter as Tkinter
from GA import GA
import folium
import math
 
class TSP(object):
    def __init__(self, searchSet, aLifeCount = 100):
        self.citys = searchSet
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate = 0.9, 
            aMutationRate = 0.07,
            aLifeCount = self.lifeCount, 
            aGeneLength = len(self.citys),
            aMatchFun = self.matchFun())

    def distance(self, order):
        distance = 0.0
        #i从-1到32,-1是倒数第一个
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

        return distance
 
    #适应度函数，因为我们要从种群中挑选距离最短的，作为最优解，所以（1/距离）最长的就是我们要求的
    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)


    def run(self, firstCity, colorChoice, fileName, n = 0):
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            if n %10 ==0:
                print (("%d : %f") % (self.ga.generation, distance))
                print (self.ga.best.gene)
            n -= 1
                  
                  
        print(self.ga.best.gene)
        print ("经过%d次迭代，最优解距离为：%f"%(self.ga.generation, distance))
        print ("遍历城市顺序为：")
        # print "遍历城市顺序为：", self.ga.best.gene
        #打印出我们挑选出的这个序列中
        for i in self.ga.best.gene:
            print(self.citys[i][2], end='->')
                
        #设定起始城市      
        while self.ga.best.gene[0] != firstCity :
            kkk = self.ga.best.gene.pop(0)
            self.ga.best.gene.append(kkk)

                  
                  
                  
            m = folium.Map(location=[34.27, 108.95], zoom_start=4)
            
            locations = []
            locationName = []
            
            
            for i in self.ga.best.gene:
                locations.append([self.citys[i][1],self.citys[i][0]])
                locationName.append(self.citys[i][2])

            for i in range(len(locations)) :
                folium.Marker(locations[i], popup=locationName[i] + str(i) , icon = folium.Icon(color="green")).add_to(m)

    
            locations.append(locations[0])
    
            ls = folium.PolyLine(locations=locations , color=colorChoice)

            ls.add_to(m)
            
            m.save(fileName)
                  
            return self.ga.best.gene
 
def main():
    
    citys = []
    searchSet = []
    
    f=open("citys.txt","r")
    while True:
        #一行一行读取
        loci = str(f.readline())
        if loci:
            pass  # do something here
        else:
            break
        #用readline读取末尾总会有一个回车，用replace函数删除这个回车
        loci = loci.replace("\n", "")
        #按照tab键分割
        loci=loci.split("\t")
        # 中国34城市经纬度读入citys
        citys.append((float(loci[1]),float(loci[2]),loci[0]))
        
        
    for k in range(len(citys)):
        print(str(k) + ":" + str(citys[k][2]) + "\t")
        
    cityNum = input("请输入搜索集合（使用空格隔开），默认使用全部的搜索集合\n")
    
    if cityNum == "":
        searchSet = citys.copy()
    else :
        for n in cityNum.split(" "):
            searchSet.append(citys[int(n)])
            
    maxNum = math.factorial(len(searchSet)-1)
    searchNum = int(input("请输入搜索路径次数,不能超过" + str(maxNum) + "次 \n"))
    firstCity = int(input("请输入起始城市的编号，编号一定要在搜索集合内\n"))
    colorSet = ['#00ff00', '#000000', '#330000', '#660000', '#666600', '#cc0000', '#ccff00', '#ff0000', '#ffcc00', '#000066','#00ff66','#0000cc','#00ffcc','#00ffff','#cc0066','#cc00ff','#ccffff','#ff00ff','#99ff99','#ffff66']
    
    
    for ret in range(searchNum):
        fileName = "tsp" + str(ret) + ".html"
        colorChoice = random.choice(colorSet)
        tsp = TSP(searchSet)
        tsp.run(firstCity, colorChoice,fileName, 3000) #默认迭代次数 
        
                
    
 #   i = []
 #   tsp = TSP()
 #   i = tsp.run(10000)
    
 #   print(i)
 
 
if __name__ == '__main__':
    main()
    print("\n")

