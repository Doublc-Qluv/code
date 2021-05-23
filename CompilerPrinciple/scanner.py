import sys
import turtle
import math
import random
import matplotlib.pyplot as plt
import numpy as np



#中文显示
plt.rc('font', family='SimHei', size=7)
#负数坐标显示
plt.rcParams['axes.unicode_minus']=False  

######################词法分析器######################
#字典栈   token_table  
#读取源文件    class read_file()
##记号的数据类   class scanner_Token()
#词法分析器DFA    class scanner()

#词法分析器测试程序  scanner_main()

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



#读取源代码文件内容
class read_file(object):
    def __init__(self):
        self.read()

    def read(self):
        self.file_name_location=input('请输入文件的位置:')
        try:
            self.file_content=open(self.file_name_location,'r',encoding='utf-8')
        except:
            print('打开明文文件失败！\n')
        else:
            self.line_content=self.file_content.read()
            self.line_content=self.line_content.upper()+'@'
            self.file_content.close()

#记号的数据类定义
class scanner_Token(object):
    def __init__(self,type=None,word=None,lexeme=None):
        self.type=type
        self.values=word   #属性，记号的输入的值
        self.lexeme=lexeme   #属性，常数的值

#词法分析器 DFA
class scanner(object):
    def __init__(self):
        self.content=read_file().line_content

    def token_type_get(self):
        self.content=iter(self.content)   #源代码的迭代器
        ch=self.content.__next__()
        while ch is not '@':
            self.word=[]     #记号缓存
            ####WHITE_SPACE   去除空格
            while ch in [' ','\n','\t','\r']:
                ch=self.content.__next__()
                if ch is '@':
                    item=scanner_Token('NONTOKEN','@',0)
                    yield item
            if ch.isalnum():
                if ch.isdigit():
                    ####数字CONST_ID
                    while True:
                        #if ch.isdigit() or ch=='.':    错误
                        if ch.isdigit():
                            self.word.append(ch)
                            ch=self.content.__next__()
                        else:
                            break
                    if ch is '.':
                        self.word.append(ch)
                        ch=self.content.__next__()
                        while True:
                            if ch.isdigit():
                                self.word.append(ch)
                                ch=self.content.__next__()
                            else:
                                break
                    item=scanner_Token('CONST_ID',''.join(self.word),float(''.join(self.word)))
                    yield item
                elif ch.isalpha():
                    ####常量名ID
                    while True:
                        if ch.isalpha():
                            self.word.append(ch)
                            ch=self.content.__next__()
                        else:
                            break
                    self.word=''.join(self.word)
                    for i in token_table:
                        if i[1]==self.word.upper():
                            item=scanner_Token(i[0],self.word,i[2])
                            yield item                  
            else:
                #注释和运算符
                if ch  is '/':
                    ch=self.content.__next__()
                    if ch is '/':
                        ####注释COMMET  '//'    过滤
                        while ch not in ['\n','@']:
                            ch=self.content.__next__()
                    else:
                        ####除号DIV
                        item=scanner_Token('DIV','/',0)
                        yield item
                elif ch is '-':
                    ch = self.content.__next__()
                    if ch is '-':
                         ####注释COMMENT  '--'   过滤
                         while ch not in ['\n','@']:
                             ch=self.content.__next__()
                    else:
                        ####减号 MINUS '-'
                        item=scanner_Token('MINUS','-',0)
                        yield item
                elif  ch is '*':
                    ch =self.content.__next__()
                    if ch is '*':
                        ####POWER  '**'
                        item=scanner_Token('POWER','**',0)
                        yield item
                    else:
                        ####MUL  '*'
                        item =scanner_Token('MUL','*',0)
                        yield item
                elif ch is '+':
                    ####PLUS  '+'
                    item =scanner_Token('PLUS','+',0)
                    ch=self.content.__next__()       #注意
                    yield item
                #分隔符
                elif ch is ';':
                    ####SEMICO ';'
                    item =scanner_Token('SEMICO',';',0)
                    ch=self.content.__next__()
                    yield item
                elif ch is ',':
                    ####COMMA  ','
                    item =scanner_Token('COMMA',',',0)
                    ch=self.content.__next__()
                    yield item
                elif ch is '(':
                    ####L_BRACKET  '('
                    item =scanner_Token('L_BRACKET','(',0)
                    ch=self.content.__next__()
                    yield item
                elif ch is ')':
                    ####R_BRACKET  ')'
                    item =scanner_Token('R_BRACKET',')',0)
                    ch=self.content.__next__()
                    yield item
                else:
                    ####错误？？？
                    item =scanner_Token('ERRTOKEN',ch,ord(ch))
                    ch=self.content.__next__()
                    yield item

def scanner_main():
    #词法分析器测试
    token_list=scanner().token_type_get()
    print(token_list)
    print("记号类型           字符串        常数值")
    print('---------------------------------------')
    for i in token_list:
        print('%9s,%12s,%12s'%(i.type,i.values,i.lexeme))



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
            print('记号识别完成，全部符合此法和语法！')
            #########################################################
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
        print(self.draw_x,self.draw_y)
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
    #词法测试
    #scanner_main()

    #语法测试
    #my_scanner=scanner()
    #my_parser=parser(my_scanner)
    #my_parser.fetchToken()
    #my_parser.program()

    #语义测试
    my_scanner=scanner()
    mysemantics=semantics(my_scanner)
    print('3')
    mysemantics.draw()
    print('4')

