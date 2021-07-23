# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
数据库模型表
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime, Float
from contentDb.database import Base


class ContentCatalogList(Base):
    __tablename__ = "contentcataloglist"
    cid = Column(String(255), primary_key=True, index=True, nullable=False)
    uid = Column(String(255), default=None)
    pid = Column(String(255), default=None)
    author = Column(String(255), default=None)
    title = Column(String(255), default=None)
    description = Column(String(255), default=None)
    publisher = Column(String(255), default=None)
    publishid = Column(String(255), default=None)
    isencrypt = Column(Integer ,default=None)
    size = Column(Float, default=None)
    content_hash = Column(String(255), default=None)
    state = Column(Integer ,default=None)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, default=None)

class ContentObjectLocation(Base):
    __tablename__ = "contentobjectlocation"
    cid = Column(String(255), primary_key=True, index=True, nullable=False)
    nid1 = Column(String(255), index=True, default=None)
    nid2 = Column(String(255), index=True, default=None)
    nid3 = Column(String(255), index=True, default=None)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, default=None)

class ContentUseTransaction(Base):
    __tablename__ = "contentusetransaction"
    id = Column(Integer, primary_key = True, autoincrement = True)
    cid = Column(String(255), index=True, nullable=False)
    uid = Column(String(255), default=None)
    value = Column(Float, default=None)
    transactionHash = Column(String(255), default=None)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, default=None)

class NodeInformation(Base):
    __tablename__ = "nodeinformation"
    nid = Column(String(255), primary_key=True, index=True)
    public_key = Column(String(255), default=None)
    node_type = Column(Integer ,default=None)
    capacity = Column(Float, default=None)
    score = Column(Integer ,default=None)
    pid = Column(String(255), default=None)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, default=None)
