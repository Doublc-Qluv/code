from io import StringIO
import string

plaintext_ = string.ascii_lowercase
ciphertext_ = string.ascii_uppercase

class creategcd(object):
    def __init__(self, key1,key2):
        self.a = key1
        self.b = key2
        self.m = 26

    def gcd(self,a,b):
        while a!=0:
            a,b = b%a,a
        return b

    def findModReverse(self,a,m):#这个扩展欧几里得算法求模逆，辗转相除法

        if self.gcd(a,m)!=1:
            return None
        u1,u2,u3 = 1,0,a
        v1,v2,v3 = 0,1,m
        while v3!=0:
            q = u3//v3
            v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
        return u1

    def classprint(self):
        result = self.findModReverse(self.a,self.m)
        return result


def encryption(plaintext,a,b):
    cipherarr = [0 for i in range(len(plaintext))]
    plaintext_list = list(plaintext)

    j = 0
    for plaintext_item in plaintext_list:
        for i in range(len(plaintext_)):
            if plaintext_item == plaintext_[i]:
                ciphertext = (11*i+4)%26
                cipherarr[j] = ciphertext_[ciphertext]
                j = j+1

    cipher = (''.join('%s'%id for id in cipherarr))
    return cipher



#解密算法
def decryption(ciphertext,a,b):
    plaintext_arr = [0 for i in range(len(ciphertext))]
    cipherlist = list(ciphertext)

    j = 0
    for cipheritem in cipherlist:
        for i in range(len(ciphertext_)):
            if cipheritem == ciphertext_[i]:
                plaintext = ((-7)*i-4)%26
                plaintext_arr[j] = plaintext_[plaintext]
                j = j+1
            else:
                pass
    plain =(''.join('%s'%id for id in plaintext_arr))
    return plain

def main():
    print('E(x) = (ax+b) mod m\nD(x) = (a^-1)(x-b) mod m\n')
    while True:
        choice=input('请输入需要的操作(gcd/encrypt/decrypt):')
        if choice == 'gcd':
            create = int(input('输入数字a:'))
            a1 = creategcd(create,26).classprint()
            print('a的模逆是:',a1)
        elif choice=='encrypt':
            plaintext = input('请输入明文：')            
            t = input('请输入a和b').split()
            a, b = int(t[0]), int(t[1])
            cipher = encryption(plaintext,a,b)
            if plaintext == 'exit':
                break
            print ('密文输出:%s'%cipher)
        elif choice=='decrypt':
            ciphertext = input('请输入密文：')
            t = input('请输入a^和b').split()
            a, b = int(t[0]), int(t[1])
            plain = decryption(ciphertext,a,b)
            if ciphertext == 'exit':
                break
            print ('明文输出:%s'%plain)
        else:
            print('Error')
if __name__ == "__main__":
    main()