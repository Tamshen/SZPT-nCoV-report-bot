from Crypto.Cipher import AES
import base64
import random
import math


class AESCipher:

    def __init__(self, key):
        self.key = key[0:16].encode('utf-8')  # 只截取16位
        self.iv = self.random_string(16).encode()  # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。

    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, text):
        """加密"""
        raw = self.random_string(64) + text
        raw = self.__pad(raw).encode()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))

    @staticmethod
    def random_string(length):
        aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
        aes_chars_len = len(aes_chars)
        retStr = ''
        for i in range(0, length):
            retStr += aes_chars[math.floor(random.random() * aes_chars_len)]
        return retStr
