# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter.messagebox import showerror
import multiprocessing
import GUI 
plt.rcParams['font.sans-serif']=['SimHei']

#best_live为每次迭代中种群最优秀的
global best_life ; best_life = None
#sum_fitness为总的适应度 ，crossRate为交叉概率， mutationRate为变异概率，crossCount,mutationCount为各自计数器
global sum_fitness , crossCount ,mutationCount , crossRate , mutationRate
crossCount = 0 ; mutationCount = 0
crossRate = 0.7 ; mutationRate = 0.02
#进化代数计数器
global generationCount ; generationCount = 1
#进化次数
global itter_time ; itter_time = 50
#种群规模
global lifecount ;  lifecount = 100
#初始点
global origin ,show_num
city_name = []
city_graph =[]
num_list = []
#载入数据

with open('citys.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(' ')
        city_name.append(line[0])
        city_graph.append([float(line[1]),float(line[2])])

#=======阶乘===============
def mul(num):
    mulsum = 1
    for i in range(1,num+1):
        mulsum *= i
    return mulsum
#==========从前端获取信息===============
#====origin为起点城市，num_list为城市列表，lifecount为种群规模
def get_route_info(city):
    global num_list , origin ,lifecount 
    origin = city_name.index(city[0])
    #==如果经历全部城市=====
    if city[1] == 'all':
        num_list = [x for x in range(len(city_name))]
    else:
        city = city[1:]
        for i in city:
            num_list.append(city_name.index(i))
        if origin not in num_list:
            num_list.append(origin)
#========num_list为经过的城市序号列表=======
    if mul(len(num_list)) < 100:
        lifecount = mul(len(num_list))
    else:
        pass
#===========求个体的距离================
def get_total_distance_2(order):
    distance = 0.0
    for i in range(0,len(num_list) - 2):
        index1 , index2 = order[i] , order[i+1]
        city1 , city2 = city_graph[index1] , city_graph[index2]
        distance += math.sqrt(pow((city1[0]-city2[0]),2)+pow((city1[1]-city2[1]),2))
    city1 , city2 = city_graph[origin] , city_graph[order[0]]
    distance += math.sqrt(pow((city1[0]-city2[0]),2)+pow((city1[1]-city2[1]),2))
    city3 = city_graph[order[-1]]
    distance += math.sqrt(pow((city1[0]-city3[0]),2)+pow((city1[1]-city3[1]),2))
    return distance
#========求舒适度======================    
def fitness_2(order):
    return 1.0 / get_total_distance_2(order)
#========种群初始化====================
#========起点先固定，其他点参与遗传=====
def init_population_2():
    population = []
    for i in range(lifecount):
        index = [x for x in num_list]
        index.remove(origin) 
        #将除起点外的其他城市点随机排序，生成染色体   
        random.shuffle(index)   
        population.append(index)
    return population
#=======挑选每代种群中最优秀的个体======
def judge_2(population):
    global sum_fitness , best_life
    sum_fitness = 0.0
    best_life = population[0]
    for i in population:
        sum_fitness += fitness_2(i)
        if(fitness_2(i) > fitness_2(best_life)):
            best_life = i
#==========交叉=====================
# 当后代的舒适度大于父代或100次之后返回，提高迭代效率
def cross_2(parent1 , parent2):
    global crossCount
    n = 0
    while 1:
        index1 = random.randint(0 , len(num_list)-2)
        index2 = random.randint(index1 , len(num_list)-2)
        gene_segment = parent2[index1 : index2]
        newGene = []
        _len = 0
        for g in parent1:
            if _len == index1:
                newGene.extend(gene_segment)
                _len += 1
            if g not in gene_segment:
                newGene.append(g)
                _len += 1
        if fitness_2(newGene) > max(fitness_2(parent1) , fitness_2(parent2)):
            crossCount += 1 
            return newGene
        if (n > 3*len(num_list)):
            crossCount += 1
            return newGene
        n += 1
#==========变异===================
#===变异时将对应位置交换，如果舒适度变高，返回=======
def mutation_2(parent):
    global mutationCount
    index1 = random.randint(0 , len(num_list)-2)
    index2 = random.randint(0 , len(num_list)-2)
    newGene = parent[:]
    newGene[index1] , newGene[index2] = newGene[index2] ,newGene[index1]
    if(fitness_2(newGene) > fitness_2(parent)):
        mutationCount += 1
        return newGene
    else:   
        rate = random.random()
        if rate < math.exp(-10 / math.sqrt(itter_time)):
            mutationCount += 1
            return newGene
        return parent
#======轮盘赌，挑选一个个体==========
def select_2(population):
    global sum_fitness
    r = random.uniform(0,sum_fitness)
    for live in population:
        r -= fitness_2(live)
        if r < 0 :
            return live
    raise Exception("选择错误",sum_fitness)
#======产生新的子代================
#方式：变异，交叉，直接遗传，先选择，后进行newChild
def newChild_2(population):
    parent1 = select_2(population)
    rate = random.random()
    
    if rate < crossRate :
        parent2 = select_2(population)
        newChild = cross_2(parent1,parent2)
    else:
        newChild = parent1[:]
    
    rate = random.random()
    if rate < mutationRate :
        newChild = mutation_2(parent1)
    
    return newChild
#========产生新代种群===========
#先仅保留上代最优秀个体，剩余用产生下一代的方法，直至种群数满
def  nextgeneration_2(population):
    global generationCount
    global best_life 
    new_population = []
    judge_2(population)
    new_population.append(best_life)
    
    while len(new_population) < lifecount :
        new_population.append(newChild_2(population))
    population = new_population
    generationCount += 1
    return population

#========绘图==================
#===调用进程，画出最后的最优解或多个优解
def draw(one_life,num_list_1,i,distance):
    ##############################
    root = tk.Tk()
    root.title("way{} distance:{}".format(i,distance))
    figure = Figure(figsize=(5,4),dpi = 100)
    a = figure.add_subplot(111)
    ##################################
    X1=[]
    Y1 = []
    for i in range(len(city_name)):
        X1.append(city_graph[i][0])
        Y1.append(city_graph[i][1])
        a.annotate(city_name[i], xy = (X1[i],Y1[i]),xytext = (X1[i]+0.1, Y1[i]+0.1))
    a.scatter(X1,Y1)
    #################################3
    X = []
    Y = []
    k = 0
    for i in one_life:
        print('{}'.format(city_name[i].encode("utf-8").decode("utf-8")),end = '')
        if(i == one_life[0] and k>0):
            pass
        else:
            print("->",end='')
        X.append(city_graph[i][0])
        Y.append(city_graph[i][1])
        k += 1
    print("\n")
    
    count = 0
    order = 1
    for j in range(len(num_list_1)):
        a.plot((X[j],X[j+1]),(Y[j],Y[j+1]),color = 'red'\
                if count == 0 else 'green')
        line_mid = ((X[j]+X[j+1])/2 , (Y[j] + Y[j+1])/2)
        a.annotate(str(order), xy = line_mid,xytext = (-8,-4),\
                     textcoords='offset points',fontsize=12,color = 'red' if count ==0 else 'green')
        count = 1 - count
        order += 1
    a.axis('equal')
    canvas = FigureCanvasTkAgg(figure,master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP,fill = tk.BOTH,expand = 1)
    toolbar = NavigationToolbar2Tk(canvas,root)
    toolbar.update()
    canvas._tkcanvas.pack(side = tk.TOP,fill = tk.BOTH,expand=1)
    def _quit():
        root.destroy()
    button = tk.Button(root,text='退出',command=  _quit)
    button.pack(side=tk.BOTTOM)
    tk.mainloop()
#========运行===============
#==迭代指代代数后，启用进程将结果绘出==
def run_2(num):
    show_y = []
    global show_num
    global best_life , num_list 
    num_list_1 = num_list[:]
    population = init_population_2()
    while num > 0:
        population = nextgeneration_2(population)
        distance = get_total_distance_2(best_life)
        #show_y.append(fitness_2(best_life))
        #print(("代数%d ")%(generationCount-1))
        print(("代数%d : distance %f")%(generationCount-1,distance))
        num -= 1

    tmp = []
    maps = []
    '''show_x = [x for x in range(100)]
    plt.plot(show_x,show_y)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title(" Generation&& Fitness")
    plt.show()'''
    for i in range(len(population)):
        #population[i] = [origin] + population[i]
        if population[i] not in tmp:
            tmp.append(population[i])
    population = sorted(tmp,key = lambda x:get_total_distance_2(x),reverse=False)
    show_num = show_num if len(population) > show_num else len(population)
    print(show_num)
    for i in range(show_num):
        distance = get_total_distance_2(population[i])
        population[i] = [origin] + population[i]
        population[i].append(population[i][0])
        maps = multiprocessing.Process(target = draw ,args = (population[i],num_list_1,i,distance))
        maps.start()
#=======程序启动==========
def do():
    global show_num
    show_num ,city = GUI.main()
    get_route_info(city)
    run_2(50)

if __name__ =='__main__':
    do()


##############前端###########标签==========GUI.py
