# -*- coding:utf-8 -*-
import random
import numpy
import scipy.io

# locate where the nearest vertices is for the randomly choosen point
def min_ocilide_distace(random_vertice,vertice_set):
    distance_set = [numpy.linalg.norm([j - k for j, k in zip(m, n)])
                  for m, n in zip(vertice_set, len(vertice_set) * [random_vertice])]
    result = distance_set.index(numpy.min(distance_set))   # ？？这里是否存在先后顺序？？？
    return result

def find_path(path,vertice_number,vertice_set):
    which_number=vertice_number
    vertice_order=[vertice_number]
    trajectory_order = []
    cishu=0
    while which_number!=0:  #0represent the start
        cishu+=1
        which_number=path[which_number-1][0]
        vertice_order.append(which_number)
    vertice_order=reversed(vertice_order)
    trajectory_order.append(vertice_set[i] for i in vertice_order)
    return trajectory_order

# load map, free space o ; obstacle space 1
def rrt(start,end,height,width,data1):
    integrated_space=[]
    free_space=[]
    obstacle_space=[]

    for i in range(0, height):
        for j in range(0, width):
            integrated_space.append([i,j])
            if data1[i][j] == 0:
                free_space.append([i,j])
            if data1[i][j] == 1:
                obstacle_space.append([i,j])

    random_cishu=0
    max_random_cishu=2000
    chazhishu=40
    initial_vertice=[round(q) for q in start]
    target_vertive=[round(q) for q in end]
    vertice_set=[initial_vertice]
    radius=40
    next_vertice=[]
    vertice_number=0
    path=[]
    distance_set=[]

    while next_vertice!=target_vertive:
    #produce random point,vertify it and the find a ner_vertices，at the same time, add to a new_path
        random_cishu+=1
        print(random_cishu)
        if random_cishu>max_random_cishu:
            print("soory!sir!path not found, because not enough random point ")
            break
        y=random.randint(0, height-1)
        x=random.randint(0, width-1)
        random_veritce = [y, x] #note here!! not [x,y]!!
        near_vertice=vertice_set[min_ocilide_distace(random_veritce,vertice_set)]
    # find a new vertice
    # a very important step is mommited here !! F-word
    # that random_vertice choosen (random or target) should be decided!!
        if random.random() < 0.4:
            random_veritce = target_vertive
            # radius = numpy.linalg.norm(numpy.array([j - k for j, k in zip(random_veritce, near_vertice)]))
        near2next_vector=[i - j for i,j in zip(random_veritce,near_vertice)]
        #to get norm2 , first transform the list to array,using numpy.array. and the original list remains unchanged
        standard_vector=[radius*i/numpy.linalg.norm(numpy.array(near2next_vector), ord=2)
                         for i in near2next_vector]
        if [round(p) for p in [i+j for i, j in zip(next_vertice,standard_vector)]] not in integrated_space:
            standard_vector=near2next_vector
        #inner-point collision detection
        #first step, all the points on the edge are in free space
        chazhicishu=0
        distance=0
        while chazhicishu != chazhishu:
            chazhicishu += 1
            inner_point = [round(q) for q in [chazhicishu / chazhishu * j + k for j, k in zip(standard_vector, near_vertice)]]
            if inner_point in obstacle_space:
                if chazhicishu == 1:
                    break
                else:
                    print('sorry, inner point in obstacle!')
                    next_vertice = next_vertice #using the former ninner point as the next_vetice
                    distance = distance #using the former ninner point as the next_vetice
                    vertice_number = vertice_number + 1
                    path.append([min_ocilide_distace(random_veritce, vertice_set), vertice_number])
                    vertice_set.append(next_vertice)
                    distance_set.append(distance)
                    break
            else:
                next_vertice = inner_point
                distance = radius * chazhicishu / chazhishu
                if next_vertice == target_vertive:
                    print('congratulations！sir，path been found')
                    vertice_number = vertice_number + 1
                    path.append([min_ocilide_distace(random_veritce, vertice_set), vertice_number])
                    vertice_set.append(next_vertice)
                    distance_set.append(distance)
                    break
                else:
                    if chazhicishu < chazhishu:
                        continue
                    if chazhicishu == chazhishu:
                        print('good choice of random vertice, go go go!')
                        vertice_number = vertice_number + 1
                        path.append([min_ocilide_distace(random_veritce, vertice_set), vertice_number])
                        vertice_set.append(next_vertice)
                        distance_set.append(distance)
                        # print(vertice_set)

    return find_path(path,vertice_number,vertice_set)


def main():
  data = scipy.io.loadmat('map.mat')  # 读取mat文件，这他么是一个字典数据结构！！！
  # print(data.keys()) 查看mat文件中的所有键!得到 dict_keys(['__header__', '__version__', '__globals__', 'map'])
  data1 = data['map']
  height = len(data1)#683
  width = len(data1[0])#803
  start=[70, 80]
  end=[399, 607]
  print('the route is :' +
         str(rrt(start,end,height,width,data1)))

if __name__ == '__main__':
    main()
