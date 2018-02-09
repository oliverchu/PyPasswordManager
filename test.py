# -*- coding:utf-8 -*-

import os
import binascii
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
def write(name,type,data):
    fout = open(name,type)
    fout.write(data)
    fout.close()

class prpcrypt():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC
    def encrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        # length = 16 #AES-128    print rs.fetchall()

        # length = 24 #AES-192
        length = 32 #AES-256
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)
     
    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


if __name__ == "__main__":
    # txt = '''TEST222312312TEST2223123123TEST2223123123TEST2223123123TEST22231231233TEST222312312TEST2223123123TEST2223123123TEST2223123123TEST22231231233TEST222312312TEST2223123123TEST2223123123TEST2223123123TEST22231231233TEST222312312TEST2223123123TEST2223123123TEST2223123123TEST22231231233TEST222312312TEST2223123123TEST2223123123TEST2223123123TEST22231231233'''
    # d = binascii.b2a_base64(txt)
    # print txt
    # print d
    # print binascii.a2b_base64(d)
    # write("1","w","TEST")
    # write("2","wb","\x54\x45\x53\x54")
    
    # 读取源文件
    fin = open("d.png","rb")
    print "raw_size:",os.path.getsize("tf.zip")
    # base64源文件编码
    dat =  base64.b64encode(fin.read())
    key = "iamolivechuiamolivechuiamolivech"
    print "base64_size",len(dat)
    pc = prpcrypt(key)
    # 加密文件
    pwd = pc.encrypt(dat)
    print "encrypt_base64_size:",len(pwd)
    write("d_crypt.png","wb",pwd)
    # 解密文件
    de = pc.decrypt(pwd)
    print "decrypt_base64_size:",len(de)
    print dat == de
    # base64解码文件
    deFile = base64.b64decode(de);
    defileLength = len(deFile)
    print "raw_size",defileLength
    print "percent:%.2f" % ( float(len(pwd))/defileLength )
    fin.close()
    # 写文件
    write("d_decrypt.png","wb",deFile)
    print "Fininished"