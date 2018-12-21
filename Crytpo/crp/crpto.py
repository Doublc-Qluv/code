#! /usr/bin/env python
# -*- coding: utf-8 -*
import string

plaintext_ = string.ascii_lowercase
ciphertext_ = string.ascii_uppercase

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

    cipher = ''.join(cipherarr)
    return cipher

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

    plain = ''.join(plaintext_arr)
    return plain

while True:
    choose = raw_input('1.encode,2.decode\n')
    if choose == '1':
        plaintext = raw_input('message：')
        cipher = encryption(plaintext)
        if plaintext == 'exit':
            break
        print'cipher_is:',cipher,'\n'

    elif choose == '2':
        ciphertext = raw_input('input_cipher：')
        plain = decryption(ciphertext)
        if ciphertext == 'EXIT':
            break
        print 'message_is：',plain,'\n'
    else:
        print'error'