import sys
import turtle
import math
import random
import matplotlib.pyplot as plt
import numpy as np





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




if __name__ == "__main__":
    #词法分析
    scanner_main()