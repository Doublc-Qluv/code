import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math


global show_num
city_name = []
city_graph =[]
city = []
with open('citys.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(' ')
        city_name.append(line[0])
        city_graph.append([float(line[1]),float(line[2])])
def main():
    global city_name
    window=tk.Tk()              #实例化一个窗口
    window.title('TSP演示')   #定义窗口标题
    window.geometry('1000x1000')  #定义窗口大小
    ttk.Label(window,text = '请选择一个城市作为起始点:  ').grid(column = 1,row =1)
    ttk.Label(window,text = '请选择需要的路径数:  ').grid(column = 1,row =2)
    ttk.Label(window,text = '请选择需要经过的城市:  ').grid(column = 1,row =3)
    
    #下拉列表
    number = tk.StringVar()
    numberChosen = ttk.Combobox(window, width=12, textvariable=number, state='readonly')
    numberChosen['values'] = city_name     # 设置下拉列表的值
    numberChosen.grid(column=2, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
    numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
    
    routenum = tk.StringVar()
    routenumChosen = ttk.Combobox(window, width=12, textvariable=routenum, state='readonly')
    routenumChosen['values'] = list(range(1,4))    
    routenumChosen.grid(column=2, row=2)      
    routenumChosen.current(0)   
    
    frm = tk.Frame(window)
    click = []
    var =[]
    
    all_var = tk.IntVar()
    def select_some():
        global show_num , city
        city.append(numberChosen.get())
        show_num = int(routenumChosen.get())
        if all_var.get() == 1:
            city.append("all")
        else:
            for i in range(len(var)):
                if var[i].get() == 1 and city_name[i] not in city :
                    city.append(city_name[i])
                else:
                    pass
        window.destroy()
        #do()
    for i in range(len(city_name)):
        var.append(tk.IntVar())
        click.append(tk.Checkbutton(frm,variable=var[i],text=city_name[i],onvalue = 1,offvalue=0 ))
    for i in range(len(city_name)):
        click[i].grid(row=(i//6)+2,column=i%6,sticky="W")
    frm.grid(row=4,column = 2)
    ttk.Button(window, text="确认", command = select_some).grid(row=8,column = 2)
    
    
    
    ck_a = tk.Checkbutton(window, variable=all_var,text="全选",onvalue = 1,offvalue=0)
    
    ck_a.grid(row = 3,column = 2)
    
    lab_msg = tk.Label(window, text='请先选择开始城市，点击确定，之后再选择需要经过的城市选择数大于3，并点击确定')
    lab_msg.grid(row=7, column = 2, sticky=tk.W)
    window.mainloop()
    return show_num,city



if __name__ == '__main__':
    print(main())
