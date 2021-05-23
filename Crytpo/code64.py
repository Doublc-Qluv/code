import base64

def Convert(string):
    a=string
    temp=''.join([chr(int(b, 16)) for b in [a[i:i + 2] for i in range(0, len(a), 2)]])
    print('base64:%s\n'%(base64.b64encode(temp.encode('utf-8'))))
    return temp

def Xor(string1,string2):
    a1=int(string1,16)
    a2=int(string2,16)
    a1=hex(a1^a2)
    print('xor:',a1)

#字符概率表
ch_rat= {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}

#计算每个字符的概率
def get_rat(string):
    rat=0
    for ch in string:
        if ch in ch_rat:
            rat+=ch_rat[ch]
    return rat

#使用秘钥对字符串逐个异或
def o_xor(key,string):
    result=""
    for ch in string:
        b=chr(key^ord(ch))
        result+=b
    return result

#遍历所有可能的秘钥
def th_ch(string):
    candidate=[]
    for key in range(256):
        plaintext=o_xor(key,string)
        rat=get_rat(plaintext)
        result={'rat':rat,'plaintext':plaintext,'key':key,'string':string}
        candidate.append(result)
    return sorted(candidate, key=lambda candidate: candidate['rat'])[-1]

#解密1
def decrypher(string):
    hex_string=''.join([chr(int(b, 16)) for b in [string[i:i + 2] for i in range(0, len(string), 2)]])
    result=th_ch(hex_string)['plaintext']
    key=chr((th_ch(hex_string))['key'])
    print('plaintext:',result)
    print('key:',key)

#解密2
def decrypher2(string):
    candidate=[]
    for str in string:
        hex_string = ''.join([chr(int(b, 16)) for b in [str[i:i + 2] for i in range(0, len(str), 2)]])
        candidate.append(th_ch(hex_string))
    result=sorted(candidate,key=lambda candidate:candidate['rat'])[-1]
    print("plaintext:",result['plaintext'])
    print("key:",chr(result['key']))
    string3=[]
    for ch in result['string']:
        order=ord(ch)
        string3.extend(hex(order))
    string3=''.join(string3).replace('0x','')
    print("string:",string3)

if __name__=='__main__':
    fd=open("test.txt",'r',encoding='utf-8')
    string=[]
    while 1:
        ch=fd.readline().replace('\n','')
        string.append(ch)
        if not ch:
            break
    print('\n转为base64编码:\n')
    Convert(string[0])
    print('\n等长字符异或:\n')
    Xor(string[1],string[2])
    print('\n单字符异或加密:\n')
    decrypher(string[3])

    fd2=open("test2.txt", 'r', encoding='utf-8')
    string2=[]
    while 1:
        ch=fd2.readline().replace('\n','')
        string2.append(ch)
        if not ch:
            break
    print('\n找原字符串:\n')
    decrypher2(string2)