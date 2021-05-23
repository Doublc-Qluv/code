# -*- encoding: utf-8 -*-
 
import random
import math
#import Tkinter
from GA import GA
 
class TSP(object):
      def __init__(self, aLifeCount = 100,):
            self.initCitys()
            self.lifeCount = aLifeCount
            self.ga = GA(aCrossRate = 0.7, 
                  aMutationRate = 0.02,
                  aLifeCount = self.lifeCount, 
                  aGeneLength = len(self.citys),
                  aMatchFun = self.matchFun())
 
 
      def initCitys(self):
            self.citys = []
            #这个文件里是34个城市的经纬度
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
                  self.citys.append((float(loci[1]),float(loci[2]),loci[0]))
 
      #order是遍历所有城市的一组序列，如[1,2,3,7,6,5,4,8……]
      #distance就是计算这样走要走多长的路
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
 
 
      def run(self, n = 0):
            while n > 0:
                  self.ga.next()
                  distance = self.distance(self.ga.best.gene)
                  if n %100 ==0:
                        print (("%d : %f") % (self.ga.generation, distance))
                        print (self.ga.best.gene)
                  n -= 1
            print( "经过%d次迭代，最优解距离为：%f"%(self.ga.generation, distance))
            print("遍历城市顺序为：")
            # print "遍历城市顺序为：", self.ga.best.gene
            #打印出我们挑选出的这个序列中
            for i in self.ga.best.gene:
                  print( self.citys[i][2],end=' ')
            print('\n')
 
def main():
      tsp = TSP()
      tsp.run(1000)
 
 
if __name__ == '__main__':
      main() 