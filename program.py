# -*- coding:utf-8 -*-

import os
import sqlite3
from binascii import a2b_hex, b2a_hex

import progressbar
from Crypto.Cipher import AES
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from texttable import Texttable

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True,need)
    name = Column(String(30))
    passwords = relationship("Password")

class Password(Base):
    __tablename__ = "password"
    id = Column(Integer,primary_key=True)
    cid = Column(Integer, ForeignKey('category.id'))
    title = Column(String(20))
    website = Column(String(100))
    username = Column(String(30))
    password = Column(String(50))
    description = Column(String(100))

engine = create_engine("sqlite:///data.db",echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
new_user = Category(id = 1,name='Test')

# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()



def initDb():
    print "sqlalchemy version:",sqlalchemy.__version__
    db = create_engine("sqlite:///data.db",echo=True)
    db.text_factory = "utf-8"
    meta = MetaData(db)
    cateTable = Table('category',meta,
        Column('id',Integer,primary_key=True),
        Column('name',String(20))
    )
    if not cateTable.exists():
        cateTable.create()
    cateTable.insert().execute({
        "id":1,
        "name":"通讯社交"
    },{
        "id":2,
        "name":"编程开发"
    },{
        "id":3,
        "name":"互联网"
    },{
        "id":4,
        "name":"博客"
    },{
        "id":5,
        "name":"Wi-Fi"
    })
    rs = cateTable.select().execute()
    print rs.fetchall()

    mainTable = Table('main',meta,
        Column('id',Integer,primary_key=True),
        Column('cid',Integer),
        Column('title',String(20)),
        Column('website',Text),
        Column('username',String(30)),
        Column('password',String(50)),
        Column('description',Text)
    )
    if not mainTable.exists():
        mainTable.create()

    return cateTable,mainTable

