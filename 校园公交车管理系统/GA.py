import random

class GA():
    #最大进化代数T，交叉概率cross_rate,变异概率variation_rate,城市数量city_num,population_count种群数量
    def __init__(self,cross_rate,variation_rate,city_num,population_count,adaptabilty):
        self.CrossRate=cross_rate
        self.VariationRate=variation_rate
        self.Population_Count=population_count
        self.CityNum=city_num
        self.AdaptabiltyFUN=adaptabilty
        self.lives=[]  #种群

        self.best=None
        self.generation=1
        self.crossCount=0
        self.variationCount=0
        self.bounds=0.0
        self.initPopulation()

    #初始化种群
    def initPopulation(self):
        self.lives=[]
        for i in range(self.Population_Count):
            gene=range(self.CityNum)
            city=City(random.sample(gene,len(gene)))
            self.lives.append(city)

    #评估
    def judge(self):
        self.bounds=0
        self.best=self.lives[0]
        for i in self.lives:
            i.score=self.AdaptabiltyFUN(i)
            self.bounds+=i.score
            if self.best.score<i.score:
                self.best=i


    #交叉
    def cross(self,parent1,parent2):
        index1=random.randint(0,self.CityNum-1)
        index2=random.randint(index1,self.CityNum-1)
        tempcity=parent1.gene[index1:index2]
        newGene=[]
        pilen=0
        for i in parent1.gene:
            if pilen==index1:
                newGene.extend(tempcity)
                pilen+=1
            if i not in tempcity:
                newGene.append(i)
                pilen+=1
        self.crossCount+=1
        return newGene

    #突变
    def variation(self,gene):
        index1=random.randint(0,self.CityNum-1)
        index2=random.randint(0,self.CityNum-1)
        gene[index1],gene[index2]=gene[index2],gene[index1]
        self.variationCount+=1
        return gene

    #选择一个个体？？？
    def getOne(self):
        """
        r=random.uniform(0,self.bounds)
        for i in self.lives:
            r-=i.score
            if r<=0:
                return i
        """
        return random.choice(self.lives)

    #产生新的后代
    def newChild(self):
        parent1=self.getOne()
        rate=random.random()

        #按概率交叉
        if rate<self.CrossRate:
            #交叉
            parent2=self.getOne()
            gene=self.cross(parent1,parent2)
        else:
            gene=parent1.gene

        #按概率突变
        rate=random.random()
        if rate<self.VariationRate:
            gene=self.variation(gene)
        
        return City(gene)

    def next(self):
        self.judge()
        newLives=[]
        newLives.append(self.best)
        while len(newLives)<self.Population_Count:
            newLives.append(self.newChild())
        self.lives=newLives
        self.generation+=1


class City():
    def __init__(self,gene,score=0):
        self.gene=gene
        self.score=score