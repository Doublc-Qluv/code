from Crypto.Cipher import AES
import base64
BS = AES.block_size


def pad(s): 
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
#定义 padding 即 填充 为PKCS7

def unpad(s): 
    return s[0:-ord(s[-1])]


class prpcrypt():  
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
    # AES的加密模式为CBC
    def encrypt(self, text):
        text = pad(text)
        cryptor = AES.new(self.key, self.mode, self.key)
        #第二个self.key 为 IV 即偏移量
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)  # 不满16，32，64位补0
        print(text)
        self.ciphertext = cryptor.encrypt(text)
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        out = unpad(st)
        return out


pc = prpcrypt('ningbozhihuirend')  # 自己设定的密钥
e = pc.encrypt("hello")  # 加密内容
d = pc.decrypt(e)
print("加密后%s,解密后%s" % (e, d))