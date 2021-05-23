# -*- coding: utf-8 -*-  
  
"""GA.py 
 
�Ŵ��㷨�� 
"""  
  
import random  
from Life import Life  
  
class GA(object):  
  
    def __init__(self, xRate = 0.7, mutationRate = 0.005, lifeCount = 50, geneLength = 100, judge = lambda lf, av: 1, save = lambda: 1, mkLife = lambda: None, xFunc = None, mFunc = None):  
        self.xRate = xRate  
        self.mutationRate = mutationRate  
        self.mutationCount = 0  
        self.generation = 0  
        self.lives = []  
        self.bounds = 0.0 # �÷�����  
        self.best = None  
        self.lifeCount = lifeCount  
        self.geneLength = geneLength  
        self.__judge = judge  
        self.save = save  
        self.mkLife = mkLife    # Ĭ�ϵĲ��������ĺ���  
        self.xFunc = (xFunc, self.__xFunc)[xFunc == None]   # �Զ��彻�溯��  
        self.mFunc = (mFunc, self.__mFunc)[mFunc == None]   # �Զ�����캯��  
  
        for i in range(lifeCount):  
            self.lives.append(Life(self, self.mkLife()))  
  
    def __xFunc(self, p1, p2):  
        # Ĭ�Ͻ��溯��  
        r = random.randint(0, self.geneLength)  
        gene = p1.gene[0:r] + p2.gene[r:]  
        return gene  
  
    def __mFunc(self, gene):  
        # Ĭ��ͻ�亯��  
        r = random.randint(0, self.geneLength - 1)  
        gene = gene[:r] + ("0", "1")[gene[r:r] == "1"] + gene[r + 1:]  
        return gene  
  
    def __bear(self, p1, p2):  
        # ���ݸ�ĸ p1, p2 ����һ�����  
        r = random.random()  
        if r < self.xRate:  
            # ����  
            gene = self.xFunc(p1, p2)  
        else:  
            gene = p1.gene  
  
        r = random.random()  
        if r < self.mutationRate:  
            # ͻ��  
            gene = self.mFunc(gene)  
            self.mutationCount += 1  
  
        return Life(self, gene)  
  
    def __getOne(self):  
        # ���ݵ÷���������ȡ��һ�����壬���������ڸ����score����  
        r = random.uniform(0, self.bounds)  
        for lf in self.lives:  
            r -= lf.score;  
            if r <= 0:  
                return lf  
  
    def __newChild(self):  
        # �����µĺ��  
        return self.__bear(self.__getOne(), self.__getOne())  
  
    def judge(self, f = lambda lf, av: 1):  
        # ���ݴ���ķ��� f ������ÿ������ĵ÷�  
        lastAvg = self.bounds / float(self.lifeCount)  
        self.bounds = 0.0  
        self.best = Life(self)  
        self.best.setScore(-1.0)  
        for lf in self.lives:  
            lf.score = f(lf, lastAvg)  
            if lf.score > self.best.score:  
                self.best = lf  
            self.bounds += lf.score  
  
    def next(self, n = 1):  
        # �ݻ�����n��  
        while n > 0:  
            # self.__getBounds()  
            self.judge(self.__judge)  
            newLives = []  
            newLives.append(Life(self, self.best.gene))  # ����õĸ������뾺��  
            # self.bestHistory.append(self.best)  
            while (len(newLives) < self.lifeCount):  
                newLives.append(self.__newChild())  
            self.lives = newLives  
            self.generation += 1  
            #print("gen: %d, mutation: %d, best: %f" % (self.generation, self.mutationCount, self.best.score))  
            self.save(self.best, self.generation)  
  
            n -= 1  