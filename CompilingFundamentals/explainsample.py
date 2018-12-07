# expl
import tokenize
from StringIO import StringIO

def parse(text):
    # 将text以StringIO的形式读入内存
    # 以字符串形式返回刀generate_tokens()函数中。
    tokens = tokenize.generate_tokens(StringIO(text).readline)
    # generate_tokens 生成器生成一个5元组：标记类型、标记字符串、标记开始位置二元组、标记结束位置二元组以及标记所在的行号
    # 下面大写的单词都属于token模块的常量
    for toknum, tokval, _, _, _ in tokens:
        if toknum == tokenize.NUMBER:
            yield int(tokval)
        elif toknum in [tokenize.OP, tokenize.STRING, tokenize.NAME]:
            yield int(tokval)
        elif tokun == tokenize.ENDMARKER:
            break
        else:
            raise RuntimeError("Unknown token %s: '%s'" % (tokenize.tok_name[toknum], tokval))
