def encryption(plaintext):# 加密算法
    cipherarr = [0 for i in range(len(plaintext))]
    plaintext_list = list(plaintext)

    j = 0
    for plaintext_item in plaintext_list:
        for i in range(len(plaintext)):
            if plaintext_item == plaintext[i]:
                ciphertext = (11*i+4)%26
                cipherarr[j] = ciphertext[ciphertext]
                j = j+1

    cipher = ''.join(cipherarr)
    return cipher

