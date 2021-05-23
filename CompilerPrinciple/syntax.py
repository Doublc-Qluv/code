import sys
import turtle
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from lexing import scanner_Token
from lexing import read_file
from lexing import scanner

#scanner_main()

###################################语法分析器###################################
#语法树类的定义   class Node()
#语法树的构造和输出  class parser_tree():
#语法分析器  class parser()
##语法分析其测试程序  def parser_main():
    

class Node(object):
    def __init__(self,data=None,values=None):
        self.data=data
        self.values=values
        self.left=None
        self.right=None
        self.child=None

#语法树
class parser_tree(object):
    def make_tree(self,token_type=None,arg1=None,arg2=None):
        if token_type is 'CONST_ID':
            t=Node(token_type,arg1)
        elif token_type is 'T':
            t=Node('T',0)
        elif token_type is 'FUNC':
            t=Node('FUNC',arg1)
            t.child=arg2
        else:
            t=Node(token_type)
            t.left=arg1
            t.right=arg2
        return t
    
    def print_tree(self,root=None,indent=None):
        for x in range(indent):
            print(' ',end='')
        if root.data is 'PLUS':
            print('+')
        elif root.data is 'MINUS':
            print('-')
        elif root.data is 'MUL':
            print('*')
        elif root.data is 'DIV':
            print('/')
        elif root.data is 'POWER':
            print('**')
        elif root.data is 'FUNC':
            print(root.values)
        elif root.data is 'CONST_ID':
            print(root.values)
        elif root.data is 'T':
            print('T')
        else:
            exit('错误的树节点')
        if root.data in ['CONST_ID','T']:
            return
        if root.data is 'FUNC':
            parser_tree().print_tree(root.child, indent + 2)
        else:
            parser_tree().print_tree(root.left, indent + 2)
            parser_tree().print_tree(root.right, indent + 2)

#语法分析器
class parser(object):
    #参数记号列表
    def __init__(self,scanner):
        self.it=scanner.token_type_get()    #词法分析器入口---记号
        self.token=scanner_Token()
    
    #下一个记号
    def fetchToken(self):
        self.token=next(self.it)
        if self.token.type is 'NONTOKEN':
            print('记号识别完成，全部符合词法和语法！')
            #结束端口，图像在这显示
            plt.show()
            sys.exit()
        elif self.token.type=='ERRTOKEN':
            self.scanner_token_err()
            #错误的记号
    
    #匹配类型  如果出错词法记号错误
    def matchToken(self,token_type):
        print('match_token  ',self.token.values)
        if self.token.type is not token_type:
            self.parser_err()
        self.fetchToken()
        
    #语法出错     记号的类型和预计类型不相同
    def parser_err(self):
        print("语法错误！--",self.token.values)
        sys.exit()
    
    #词法的记号出错    错误的记号，没法识别的记号
    def scanner_token_err(self):
        print('词法记号错误！---',self.token.values)
        sys.exit()
    
    #主程序
    def program(self):
        print("enter program")
        while True:
            self.statement()
            self.matchToken('SEMICO')
        print('exit program')

    #执行语句
    def statement(self):
        print("enter statement")
        if self.token.type=='ORIGIN':
            self.originstatment()
        elif self.token.type=='SCALE':
            self.scalestatment()
        elif self.token.type=='ROT':
            self.rotstatment()
        elif self.token.type=='FOR':
            self.forstatment()
        else:
            self.parser_err()
        print('exit statement')  
    
    def originstatment(self):
        print('enter originstatement')
        self.matchToken('ORIGIN')
        self.matchToken('IS')
        self.matchToken('L_BRACKET')
        self.origin_x=self.expression()
        self.matchToken('COMMA')
        self.origin_y=self.expression()
        self.matchToken('R_BRACKET')
        print('exit originstatement')

    def scalestatment(self):
        print('enter scalestatement!')
        self.matchToken('SCALE')
        self.matchToken('IS')
        self.matchToken('L_BRACKET')
        self.scale_x=self.expression()
        self.matchToken('COMMA')
        self.scale_y=self.expression()
        self.matchToken('R_BRACKET')
        print('exit scalestatement')
    
    def rotstatment(self):
        print('enter rotstatement!')
        self.matchToken('ROT')
        self.matchToken('IS')
        self.scale_x=self.expression()
        print('exit rotstatement!')        

    def forstatment(self):        
        print('enter forstatement!')
        self.matchToken('FOR')
        self.matchToken('T')
        self.matchToken('FROM')
        self.start=self.expression()
        self.matchToken('TO')
        self.end=self.expression()
        self.matchToken('STEP')
        self.step=self.expression()
        self.matchToken('DRAW')
        self.matchToken('L_BRACKET')
        self.x=self.expression()
        self.matchToken('COMMA')
        self.y=self.expression()
        self.matchToken('R_BRACKET')
        print('exit forstatement')

    def expression(self):
        print('enter expression')
        left=self.term()
        while self.token.type in ['PLUS','MINUS']:
            token_tem=self.token.type
            self.matchToken(token_tem)
            right=self.term()
            left=parser_tree().make_tree(token_tem,left,right)
        parser_tree().print_tree(left,2)
        print('exit expression')
        return left
    
    def term(self):     #局部变量和全局变量的范围---right left
        print('enter term')
        left=self.factor()
        while self.token.type in ['MUL','DIV']:
            token_tem = self.token.type
            self.matchToken(token_tem)
            right=self.factor()
            left=parser_tree().make_tree(token_tem,left,right)
        print('exit term')
        return left
    
    def factor(self):
        print('enter factor')
        if self.token.type is 'PLUS':
            self.matchToken('PLUS')
            right=self.factor()
        elif self.token.type is 'MINUS':
            self.matchToken('MINUS')
            right=self.factor()
            left=Node('CONST_ID',0)     #负数使用表达式来计算？？？？？
            right=parser_tree().make_tree('MINUS',left,right)
        else:
            right=self.component()
        print('exit factor')
        return right

    def component(self):
        print('enter component')
        left=self.atom()
        if self.token.type is 'POWER':
            self.matchToken('POWER')
            right=self.component()
            left=parser_tree().make_tree('POWER',left,right)
        print('exit component')
        return left

    def atom(self):
        tem=self.token
        if self.token.type is 'CONST_ID':
            self.matchToken('CONST_ID')
            t=parser_tree().make_tree('CONST_ID',tem.lexeme)
        elif self.token.type is 'T':
            self.matchToken('T')
            t=parser_tree().make_tree('T')
        elif self.token.type is 'FUNC':
            func_name=self.token.values
            self.matchToken('FUNC')
            self.matchToken('L_BRACKET')
            s=self.expression()
            t=parser_tree().make_tree('FUNC',func_name,s)
            self.matchToken('R_BRACKET')
        elif self.token.type is 'L_BRACKET':
            self.matchToken('L_BRACKET')
            t=self.expression()
            self.matchToken('R_BRACKET')
        else:
            exit('atom 错误')
        return t
      
def parser_main():
    #语法分析其测试程序
    my_scanner=scanner()
    my_parser=parser(my_scanner)
    my_parser.fetchToken()
    my_parser.program()


if __name__ == "__main__":
    #语法测试
    my_scanner=scanner()
    my_parser=parser(my_scanner)
    my_parser.fetchToken()
    my_parser.program()


