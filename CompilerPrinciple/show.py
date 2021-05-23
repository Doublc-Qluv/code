import sys
import turtle
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from lexing import read_file
from lexing import scanner_Token
from lexing import scanner
from syntax import Node
from syntax import parser_tree
from syntax import parser

#中文显示
plt.rc('font', family='SimHei', size=7)
#负数坐标显示
plt.rcParams['axes.unicode_minus']=False  

# 符号表内容    #可以简化
token_table =[
    ['CONST_ID',	"PI",		3.1415926],
	['CONST_ID',	"E",		2.71828],
	['T',		"T",		0.0	],
	['FUNC',		"SIN",		0.0],
	['FUNC',		"COS",		0.0],
	['FUNC',		"TAN",		0.0],
	['FUNC',		"LN",		0.0],
	['FUNC',		"EXP",		0.0],
	['FUNC',		"SQRT",		0.0],
	['ORIGIN',	"ORIGIN",	0.0],
	['SCALE',		"SCALE",	0.0],
	['ROT',		"ROT",		0.0],
	['IS',		"IS",		0.0],
	['FOR',		"FOR",		0.0],
	['FROM',		"FROM",		0.0],
	['TO',		"TO",		0.0],
	['STEP',		"STEP",		0.0],
	['DRAW',		"DRAW",		0.0]
]





#parser_main()

############################语义分析器###############################

class semantics_tree(object):
    def parser_tree_values(self,root=None,T=0):
        if root.data is 'PLUS':
            return float(semantics_tree().parser_tree_values(root.left,T))+float(semantics_tree().parser_tree_values(root.right,T))
        elif root.data is 'MINUS':
            return float(semantics_tree().parser_tree_values(root.left,T))-float(semantics_tree().parser_tree_values(root.right,T))
        elif root.data is 'MUL':
            return float(semantics_tree().parser_tree_values(root.left,T))*float(semantics_tree().parser_tree_values(root.right,T))
        elif root.data is 'DIV':
            return float(semantics_tree().parser_tree_values(root.left,T))/float(semantics_tree().parser_tree_values(root.right,T))
        elif root.data is 'POWER':
            return float(semantics_tree().parser_tree_values(root.left,T))**float(semantics_tree().parser_tree_values(root.right,T))
        elif root.data is 'FUNC':
            if root.values == 'SIN':
                return math.sin(semantics_tree().parser_tree_values(root.child,T))
            elif root.values == 'COS':
                return math.cos(semantics_tree().parser_tree_values(root.child,T))
            elif root.values is 'TAN':
                return math.tan(semantics_tree().parser_tree_values(root.child,T))
            elif root.values is 'LN':
                return math.log(semantics_tree().parser_tree_values(root.child,T))
            elif root.values is 'EXP':
                return math.exp(semantics_tree().parser_tree_values(root.child,T))
            elif root.values is 'SQRT':
                return math.sqrt(semantics_tree().parser_tree_values(root.child,T))
            else:
                print('函数输入错误！')
                sys.exit()
        elif root.data is 'CONST_ID':
            return root.values
        elif root.data is 'T':
            return T
        else:
            return 0

#语义解释器
class semantics(parser):
    def __init__(self,my_scanner=None):
        parser.__init__(self,my_scanner)
        self.scale_x=0    #横坐标比例
        self.scale_y=0  #纵坐标比列
        self.rot=0    #角度
        self.origin_x=0   #初始点横坐标值
        self.origin_y=0 #初始化纵坐标值
        self.start=0  #起始值
        self.end=0      #结束值
        self.step=0    #步长
        self.x=0   #横坐标
        self.y=0   #纵坐标


    def originstatment(self):
        print('enter originstatement')
        self.matchToken('ORIGIN')
        self.matchToken('IS')
        self.matchToken('L_BRACKET')
        tem=self.expression()
        self.origin_x=semantics_tree().parser_tree_values(tem)
        print('origin_x:  ',self.origin_x)
        self.matchToken('COMMA')
        tem=self.expression()
        self.origin_y=semantics_tree().parser_tree_values(tem)
        print('origin_y:  ',self.origin_y)
        self.matchToken('R_BRACKET')
        print('exit originstatement')

    def scalestatment(self):
        print('enter scalestatement!')
        self.matchToken('SCALE')
        self.matchToken('IS')
        self.matchToken('L_BRACKET')
        tem=self.expression()
        self.scale_x=semantics_tree().parser_tree_values(tem)
        print('scale_x:  ',self.scale_x)
        self.matchToken('COMMA')
        tem=self.expression()
        self.scale_y=semantics_tree().parser_tree_values(tem)
        print('scale_y:  ',self.scale_y)
        self.matchToken('R_BRACKET')
        print('exit scalestatement')
    
    def rotstatment(self):
        print('enter rotstatement!')
        self.matchToken('ROT')
        self.matchToken('IS')
        tem=self.expression()
        self.rot=semantics_tree().parser_tree_values(tem)
        print('self.rot: ',self.rot)
        print('exit rotstatement!')        

    def forstatment(self):        
        print('enter forstatement!')
        self.matchToken('FOR')
        self.matchToken('T')
        self.matchToken('FROM')
        tem=self.expression()
        self.start=semantics_tree().parser_tree_values(tem)
        print('start: ',self.start)
        self.matchToken('TO')
        tem=self.expression()
        self.end=semantics_tree().parser_tree_values(tem)
        print('end:  ',self.end)
        self.matchToken('STEP')
        tem=self.expression()
        self.step=semantics_tree().parser_tree_values(tem)
        print('step:  ',self.step)
        self.matchToken('DRAW')
        self.matchToken('L_BRACKET')
        self.x=self.expression()
        self.matchToken('COMMA')
        self.y=self.expression()
        self.matchToken('R_BRACKET')
        print('exit forstatement')
        self.draw_expression()
        #self.draw()

    #计算作图时用到的横纵坐标的值
    def draw_expression(self):
        self.draw_x=[]
        self.draw_y=[]
        for t in np.arange(self.start,self.end+self.step,self.step):
            self.draw_x.append(semantics_tree().parser_tree_values(self.x,t))
            self.draw_y.append(semantics_tree().parser_tree_values(self.y,t))
        print(self.draw_x,self.draw_y)
        self.draw_x=np.array(self.draw_x)
        self.draw_y=np.array(self.draw_y)
        #角度旋转---使用self.rot
        if self.rot!=0:
            tem_draw_x=self.draw_x*math.cos(self.rot)+self.draw_y*math.sin(self.rot)
            self.draw_y=self.draw_y*math.cos(self.rot)-self.draw_x*math.sin(self.rot)
            self.draw_x=tem_draw_x
        #坐标平移和比例设置
        if self.scale_x!=0  and self.scale_y!=0:
            self.draw_x=self.draw_x*self.scale_x
            self.draw_y=self.draw_y*self.scale_y
        if self.origin_x!=0 and self.origin_y!=0:
            self.draw_x=self.draw_x+self.origin_x
            self.draw_y=self.draw_y+self.origin_y
        print('1')
        plt.scatter(self.draw_x,self.draw_y,marker=',',c='r',s=1)
        # print(self.draw_x,self.draw_y)
        #plt.show()

    #启动函数------绘图函数
    def draw(self):
        #print(self)
        plt.figure(num=1,figsize=(8,6))
        plt.title('编译原理大作业')
        self.fetchToken()
        self.program()
        #plt.scatter(self.draw_x,self.draw_y)
        plt.show()



if __name__ == "__main__":
    #语义测试
    my_scanner=scanner()
    mysemantics=semantics(my_scanner)
    print('3')
    mysemantics.draw()
    print('4')

