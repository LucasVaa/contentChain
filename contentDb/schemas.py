# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
模型验证
"""
import os
import sys

from sqlalchemy.sql.expression import update
sys.path.append(os.pardir)
from pydantic import BaseModel
import datetime
from typing import List

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

class ContentCatalogListResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[ContentCatalogList]

class ContentObjectLocation(BaseModel):
    cid: str
    nid1: str
    nid2: str
    nid3: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

class ContentObjectLocationResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[ContentObjectLocation]

class ContentUseTransaction(BaseModel):
    cid: str
    uid: str
    value: float
    transactionHash: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    
    class Config:
        orm_mode = True

class ContentUseTransactionResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[ContentUseTransaction]

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

class NodeInformationResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[NodeInformation]

class changeTypeRequest(BaseModel):
    nid: str
    type: int

    class Config:
        orm_mode = True

class ContentMeta(BaseModel):
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
    createdAt: datetime.datetime

    class Config:
        orm_mode = True

class updateLocationRequest(BaseModel):
    cid: str
    nid_previous: str
    nid_current: str

    class Config:
        orm_mode = True

# 更改内容所有权的请求
class contentOwnTradeRequest(BaseModel):
    cid: str
    uid: str
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

# 下架内容和屏蔽内容的请求
class contentStateRequest(BaseModel):
    cid: str
    state: int
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

# 存储位置变更的请求
class locationUpdateRequest(BaseModel):
    cid: str
    nid_previous: str
    nid_current: str
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

# 结点删除的请求
class nodeDeleteRequest(BaseModel):
    nid_chosen: str

    class Config:
        orm_mode = True

# 结点类型更改的请求
class nodeModeModifyRequest(BaseModel):
    nid_chosen: str
    mode_current: int
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True