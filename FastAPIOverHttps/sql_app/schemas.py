# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
模型验证
"""
import os
import sys
sys.path.append(os.pardir)
from pydantic import BaseModel
import datetime

class ContentCatalogList(BaseModel):
    cid: str
    uid: str
    pid: str
    author: str
    title: str
    description: str
    publisher: str
    publishid: str
    isencrypt: int
    size: float
    content_hash: str
    state: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

class ContentObjectLocation(BaseModel):
    cid: str
    nid1: str
    nid2: str
    nid3: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

class ContentUseTransaction(BaseModel):
    cid: str
    uid: str
    value: float
    transactionHash: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    
    class Config:
        orm_mode = True

class NodeInformation(BaseModel):
    nid: str
    public_key: str
    node_type: int
    capacity: float
    score: int
    pid: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True
