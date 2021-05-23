from io import StringIO
import string
plaintext_ = string.ascii_lowercase
ciphertext_ = string.ascii_uppercase



#加密算法

def encryption(plaintext):
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
def decryption(ciphertext):
    plaintext_arr = [0 for i in range(len(ciphertext))]
    cipherlist = list(ciphertext)

    j = 0
    for cipheritem in cipherlist:
        for i in range(len(ciphertext_)):
            if cipheritem == ciphertext_[i]:
                plaintext = (19*i-24)%26
                plaintext_arr[j] = plaintext_[plaintext]
                j = j+1
            else:
                pass
    plain =(''.join('%s'%id for id in plaintext_arr))
    return plain

def main():
    while True:
        #print('请输入需要的操作（encrypt/decrypt）')
        choice=input('请输入需要的操作(encrypt/decrypt):')
        if choice=='encrypt':
            plaintext = input('请输入明文：')
            cipher = encryption(plaintext)
            if plaintext == 'exit':
                break
            print ('密文输出:%s'%cipher)
        elif choice=='decrypt':
            ciphertext = input('请输入密文：')
            plain = decryption(ciphertext)
            if ciphertext == 'exit':
                break
            print ('明文输出:%s'%plain)
        else:
            print('功能输入错误')

if __name__=='__main__':
    main()
