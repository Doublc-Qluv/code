# temp.py
from collections import deque
class Stack(deque): # 定义一个栈
    push = deque.append  # 添加元素
    # 返回最后一个元素
    def top(self):
        return self[-1]

class Machine:
    def __init__(self, code): # 预先定义一个初始化函数
       self.data_stack = Stack()
       self.return_addr_stack = Stack()
       self.code = code
       self.instruction_pointer = 0 
    # 再创建一些栈结构中必备的函数
    def pop(self):
        return self.data_stack.pop()
    def push(self, value):
        self.data_stack.push(value)
    def top(self):
        return self.data_stack.top()

def run(self):   # 代码运行的条件
    while self.instruction_pointer < len(self.code):
         opcode = self.code[self.instruction_pointer]
         self.instruction_pointer += 1
         self.dispatch(opcode)

def dispatch(self, op):
    dispatch_map = {
        "%":        self.mod,
        "*":        self.mul,
        "+":        self.plus,
        "-":        self.minus,
        "/":        self.div,
        "==":       self.eq,
        "cast_int": self.cast_int,
        "cast_str": self.cast_str,
        "drop":     self.drop,
        "dup":      self.dup,
        "if":       self.if_stmt,
        "jmp":      self.jmp,
        "over":     self.over,
        "print":    self.print_,
        "println":  self.println,
        "read":     self.read,
        "stack":    self.dump_stack,
        "swap":     self.swap,
        }
    if op in dispatch_map:
        dispatch_map[op]()
    elif isinstance(op, int):  # 如果指令是整形数据，就将数据存放到数据栈中
        self.push(op)
    elif isinstance(op, str) and op[0]==op[-1]=='"':
        # 如果是字符串类型，就将字符串内容存放到数据栈中
        self.push(op[1:-1])
    else:
        raise RuntimeError( "Unknown opcode: '%s'" % op)

def mul(self):
    self.push(self.pop() * self.pop())
'''
st=>start: 指令
op1=>operation: 解析器
op2=>operation: 词法单元
op3=>operation: 执行运算
e=>end: 结果

st->op1->op2->op3->e
'''
def constant_fold(code):
    while True:
        # 指令中找到两个连续的数字以及一个运算符
        for i, (a, b, op) in enumerate(zip(code, code[1:], code[2:])):
            if isinstance(a, int) and isinstance(b, int) and op in {"+", "-", "*", "/"}:
                m = Machine((a, b, op))
                m.run()
                code[i:i+3] = [m.top()]
                print("Constant-folded %s%s%s to %s" % (a, op, b, m.top()))
                break
        else:
            break
    return code
def repl():
    print('Hit CTRL+D or type "exit" to quit.')

    while True:
        try:
            source = raw_input("> ")
            code = list(parse(source))
            code = constant_fold(code)
            Machine(code).run()
        except (RuntimeError, IndexError) as e:
            print("IndexError: %s" % e)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
