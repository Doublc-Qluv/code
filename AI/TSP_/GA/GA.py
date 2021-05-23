# -*- coding: utf-8 -*-
 
import random
from Life import Life
 
class GA(object):
      """遗传算法类"""
      def __init__(self, aCrossRate, aMutationRate, aLifeCount, aGeneLength, aMatchFun = lambda life : 1):
            self.crossRate = aCrossRate               #交叉概率
            self.mutationRate = aMutationRate         #突变概率
            self.lifeCount = aLifeCount               #种群数量，就是每次我们在多少个城市序列里筛选，这里初始化为100
            self.geneLength = aGeneLength             #其实就是城市数量
            self.matchFun = aMatchFun                 #适配函数
            self.lives = []                           #种群
            self.best = None                          #保存这一代中最好的个体
            self.generation = 1                       #一开始的是第一代
            self.crossCount = 0                       #一开始还没交叉过，所以交叉次数是0
            self.mutationCount = 0                    #一开始还没变异过，所以变异次数是0
            self.bounds = 0.0                         #适配值之和，用于选择时计算概率
            self.initPopulation()                     #初始化种群
 

      def initPopulation(self):
            """初始化种群"""
            self.lives = []
            for _ in range(self.lifeCount):
                  # gene = [0,1,…… ,self.geneLength-1]
                  gene = list(range(self.geneLength))
                  # 将0到33序列的所有元素随机排序得到一个新的序列
                  random.shuffle(gene)
                  # Life这个类就是一个基因序列，初始化life的时候,两个参数，一个是序列gene，一个是这个序列的初始适应度值
                  # 因为适应度值越大，越可能被选择，所以一开始种群里的所有基因都被初始化为-1
                  life = Life(gene)
                  #把生成的这个基因序列life填进种群集合里
                  self.lives.append(life)
 
 
      def judge(self):
            """评估，计算每一个个体的适配值"""

            self.bounds = 0.0
            #假设种群中的第一个基因被选中
            self.best = self.lives[0]
            for life in self.lives:
                  life.score = self.matchFun(life)
                  self.bounds += life.score
                  #如果新基因的适配值大于原先的best基因，就更新best基因
                  if self.best.score < life.score:
                        self.best = life
 
      def cross(self, parent1, parent2):
            """交叉"""
            index1 = random.randint(0, self.geneLength - 1)
            index2 = random.randint(index1, self.geneLength - 1)
            tempGene = parent2.gene[index1:index2]                      #交叉的基因片段
            newGene = []
            p1len = 0
            for g in parent1.gene:
                  if p1len == index1:
                        newGene.extend(tempGene)                               #插入基因片段
                        p1len += 1
                  if g not in tempGene:
                        newGene.append(g)
                        p1len += 1
            self.crossCount += 1
            return newGene
 
 
      def  mutation(self, gene):
            """突变"""
            #相当于取得0到self.geneLength - 1之间的一个数，包括0和self.geneLength - 1
            index1 = random.randint(0, self.geneLength - 1)
            index2 = random.randint(0, self.geneLength - 1)
            #把这两个位置的城市互换
            gene[index1], gene[index2] = gene[index2], gene[index1]
            #突变次数加1
            self.mutationCount += 1
            return gene
 
 
      def getOne(self):
            """选择一个个体"""
            #产生0到（适配值之和）之间的任何一个实数
            r = random.uniform(0, self.bounds)
            for life in self.lives:
                  r -= life.score
                  if r <= 0:
                        return life
 
            raise Exception("选择错误", self.bounds)
 
 
      def newChild(self):
            """产生新后的"""
            parent1 = self.getOne()
            rate = random.random()
 
            #按概率交叉
            if rate < self.crossRate:
                  #交叉
                  parent2 = self.getOne()
                  gene = self.cross(parent1, parent2)
            else:
                  gene = parent1.gene
 
            #按概率突变
            rate = random.random()
            if rate < self.mutationRate:
                  gene = self.mutation(gene)
 
            return Life(gene)
 
 
      def next(self):
            """产生下一代"""
            self.judge()#评估，计算每一个个体的适配值
            newLives = []
            newLives.append(self.best)#把最好的个体加入下一代
            while len(newLives) < self.lifeCount:
                  newLives.append(self.newChild())
            self.lives = newLives
            self.generation += 1