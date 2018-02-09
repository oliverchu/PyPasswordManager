#coding=utf-8
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import sqlite3
import os
from texttable import Texttable
import progressbar
import sys
import getpass
from sqlalchemy import * 
import base64

def create_db():
    conn = sqlite3.connect(current_file)
    conn.text_factory = str
    print "Opened database successfully";
    conn.execute('''
        create table if not exists category(
        id integer PRIMARY KEY autoincrement,
        name text unique)
    ''')

    conn.execute('''
        create table if not exists main(
        id integer PRIMARY KEY autoincrement,
        gid integer,
        name text,
        website text,
        username text,
        pwd text,
        description text,
        foreign key(gid) references category(id)
        )
    ''')
    conn.close()
    try:
        addCategory("通讯社交")
        addCategory("编程开发")
        addCategory("互联网")
        addCategory("WiFi热点")
    except sqlite3.IntegrityError as ex:
        print ex.message



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
 
def addCategory(name):
    conn = sqlite3.connect(current_file)
    conn.execute("insert into category(name) values('%s')"%(name))
    print "Insert successfully."
    conn.commit()
    conn.close()

def listMain(category):
    conn = sqlite3.connect(current_file)
    cur = conn.execute("select * from main")
    res = cur.fetchall()
    rows = []
    rows.append(["编号","分组","标题","网址","描述","用户名","密码"])
    for c in res:
        rows.append([c[0],category[c[1]-1][1],c[2],c[3],c[6],c[4],c[5]])
    table(rows)
    conn.close()
    return res;


def listCategory():
    conn = sqlite3.connect(current_file)
    cur = conn.execute("select * from category")
    res = cur.fetchall()
    rows = []
    rows.append(["编号","组名"])
    for c in res:
        rows.append([c[0],c[1]])
    table(rows)
    conn.close()
    return res;

def addMain(data):
    conn = sqlite3.connect(current_file)
    conn.execute("insert into main(gid,name,website,pwd,username,description) values (?,?,?,?,?,?)",data)    
    conn.commit()
    conn.close()

def getGid(category,catName):
    for c in category:
        if c[1] == catName:
            return c[0]   
    return -1

def table(rows):
    table = Texttable()
    colNum = len(rows[0])
    colsAlign = []
    colsValign = []
    for c in range(colNum):
        colsAlign.append("l")
        colsValign.append("a")
    table.set_cols_align(colsAlign)
    table.set_cols_valign(colsValign)
    table.add_rows(rows)
    print table.draw() + "\n"

def get_input(text):
    return raw_input(text).decode(sys.stdin.encoding or locale.getpreferredencoding(True))

gkey = ""

def main():
    os.system("reset")
    print '''
    请选择功能
    -------------------------
    1.新建密码
    2.查看所有密码
    3.新建分类
    4.查看分类
    0.退出(q)
    -------------------------
    '''
    m_input = raw_input("您的输入>")
    try:
        while not int(m_input)>=0 and int(m_input)<4:
            m_input = raw_input("[x]您的输入>")
    except:
        pass
    pc = prpcrypt(gkey)
    print m_input
    if m_input == '0':
        print "gkey=",gkey
        encrypt(gkey)
        print "文件加密成功,退出"
        exit()
    elif m_input == '1':
        while True:
            os.system("clear")
            cat = listCategory()
            listMain(cat)
            gid = get_input("请选择一个分组>")
            name = get_input("请输入标题>")
            website = get_input("请键入网站>")
            username = get_input("请输入用户名>")
            pwd = get_input("请输入密码>")
            description = get_input("请输入描述>")
            pwd = pc.encrypt(pwd)
            dat = (gid,name,website,pwd,username,description)
            addMain(dat)
            print "保存成功，是否再次添加？（y/n）"
            ipt = raw_input()
            ipt = str(ipt).lower()
            if ipt == 'y':
                pass
            elif ipt == 'n':
                break
    elif m_input == '2':
        categlory = listCategory()
        listMain(categlory)
        raw_input("继续?")
    elif m_input == '3':
        pass
    elif m_input == '4':
        listCategory()
        raw_input("继续?")

def verify_pwd(key):
    global gkey
    gkey = fill_key(key)
    print gkey
    decrypt(gkey)
    return True

current_file = ""

def encrypt(key):
    pc = prpcrypt(key)
    fin = open(current_file,"rb")
    dat = base64.b64encode(fin.read())
    fin.close()
    pwd = pc.encrypt(dat)
    fout = open(current_file,"wb")
    # fout.write("SQLite format \x00")
    fout.write(pwd)
    fout.close()

def decrypt(key):
    pc = prpcrypt(key)
    fin = open(current_file,"rb")
    readData = fin.read()
    print readData
    pwd = pc.decrypt(readData)
    dat = base64.b64decode(pwd)
    fin.close()
    fout = open(current_file,"wb")
    fout.write(dat)
    fout.close()
    return True

def fill_key(key):
    keyLen = len(key)
    if keyLen < 32:
        for x in range(keyLen,32):
            key += "0"
    return key

def save():
    key = getpass.getpass("请输入管理密码>")     
    keyLen = len(key)
    if keyLen < 32:
        for x in range(keyLen,32):
            key += "0"
    print len(key),key
    keyLen = len(key)
    print keyLen
    if not keyLen == 16 and not keyLen == 24 and not  keyLen == 32:
        print "Key must be 16,24 or 32 bytes long, it's ",keyLen
        exit() 
    
def list_files(root):
    fileArr = []
    for root,dirs,files in os.walk(root):
        for f in files:
            if f.endswith(".db"):
                fileArr.append(f)
    return fileArr

# main function
if __name__ == '__main__':
    files = list_files("./")
    if len(files) == 0:
        print "目录下暂时没有文件,请新建文件"
        name = raw_input("文件名(*.db)>")
        while not name.lower().endswith(".db"):
            name = raw_input("[x]文件名(*.db)>")
        masterPwd = raw_input("请输入管理密码(6-32位)>")
        while not len(masterPwd) >= 6 and len(masterPwd)<=32:
             masterPwd = raw_input("[x]请输入管理密码(6-32位)>")
        masterPwdConfirm = raw_input("请再次输入管理密码>")
        while masterPwd != masterPwdConfirm:
            masterPwdConfirm = raw_input("[x]请再次输入管理密码>")
        masterPwd = fill_key(masterPwd)
        print name,masterPwd
        current_file = name
        create_db()
        encrypt(masterPwd)
        print "加密数据库 %s 成功" % (name)
    else:        
        for index,value in enumerate(files):
            print str(index)+". "+value
        sel = raw_input("请选择一个文件>")
        selIdx = int(sel)
        current_file = files[selIdx]
    pwd = getpass.getpass("请输入管理密码>")
    if verify_pwd(pwd):
        while True:
            main()
    else:
        print "管理密码错误"