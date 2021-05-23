#coding=utf-8
import time

class CaesarCipher(object):
    def __crypt(self, char, key):

        if not char.isalpha():
            return char
        else:
            base = "A" if char.isupper() else "a"
            return chr((ord(char) - ord(base) + key) % 26 + ord(base))

    def encrypt(self, char, key):
        return self.__crypt(char, key)

    def decrypt(self, char, key):
        return self.__crypt(char, -key)

    def __crypt_text(self, func, text, key):
        lines = []
        for line in text.split("\n"):
            words = []
            for word in line.split(" "):
                chars = []
                for char in word:
                    chars.append(func(char, key))
                words.append("".join(chars))
            lines.append(" ".join(words))
        return "\n".join(lines)

    def encrypt_text(self, text, key):
        return self.__crypt_text(self.encrypt, text, key)

    def decrypt_text(self, text, key):
        return self.__crypt_text(self.decrypt, text, key)


if __name__ == '__main__':
    plain = "WhatIlikeisthefuture"
    key = 3

    caesar = CaesarCipher()


    print("Encrypting......")
    start = time.clock()
    cipher = caesar.encrypt_text(plain, key)
    print("Encrypted!\r\nThe Cipher is:",cipher)
    end1 = time.clock()
    print("加密用时："+str(end1-start))

    c = cipher     
    #读取密文
    print("Decrypting......")
    plain = caesar.decrypt_text(c, key)
    print("Decrypted!\r\nThe PlainText is:",plain)
    end2 = time.clock()
    print("解密用时："+str(end2-end1))