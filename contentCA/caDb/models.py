# -*- coding:UTF-8 -*-
"""
Created on 2021年7月24日

@author: Xinhuiyang
CA数据库模型表
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime, Float
from contentCA.caDb.database import Base

# 用户信息
class UserInformation(Base):
    __tablename__ = "userinformation"
    uid = Column(String(20), primary_key=True, index=True, nullable=False)
    name = Column(String(20), default=None)
    full_name = Column(String(40), default=None)
    mail = Column(String(40), default=None)
    password = Column(String(40), default=None)
    time = Column(DateTime, nullable=False)

# 用户公钥私钥
class UserKey(Base):
    __tablename__ = "userkey"
    uid = Column(String(20), primary_key=True, index=True, nullable=False)
    public_key = Column(String(1000), default=None)
    private_key = Column(String(1000), default=None)
    time = Column(DateTime, nullable=False)

# 用户设备许可
class UserLicense(Base):
    __tablename__ = "userlicense"
    id = Column(Integer, primary_key = True, autoincrement = True)
    uid = Column(String(20), default=None)
    did = Column(String(20), default=None)

# 内容公钥私钥
class ContentKey(Base):
    __tablename__ = "contentkey"
    cid = Column(String(20), primary_key=True, index=True, nullable=False)
    content_hash = Column(String(100), default=None)
    author = Column(String(100), default=None)
    title = Column(String(100), default=None)
    pid = Column(String(20), default=None)
    aes_key = Column(String(100), default=None)
    time = Column(DateTime, nullable=False)

# 设备公钥私钥
class DeviceKey(Base):
    __tablename__ = "devicekey"
    did = Column(String(20), primary_key=True, index=True, nullable=False)
    public_key = Column(String(1000), default=None)
    private_key = Column(String(1000), default=None)
    time = Column(DateTime, nullable=False)

# 结点公钥私钥
class NodeKey(Base):
    __tablename__ = "nodekey"
    nid = Column(String(20), primary_key=True, index=True, nullable=False)
    public_key = Column(String(1000), default=None)
    private_key = Column(String(1000), default=None)
    time = Column(DateTime, nullable=False)