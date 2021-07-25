# -*- coding:UTF-8 -*-
"""
Created on 2021年7月24日

@author: Xinhuiyang
模型验证
"""
import os
import sys
sys.path.append(os.pardir)
from pydantic import BaseModel
import datetime
from typing import List

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

class ContentKey(BaseModel):
    cid: str
    content_hash: str
    author: str
    title: str
    pid: str
    aes_key: str
    time: datetime.datetime

    class Config:
        orm_mode = True

class ContentKeyReponse(BaseModel):
    resultCode: int
    msg: str
    data: List[ContentKey]

    class Config:
        orm_mode = True

class NodeKey(BaseModel):
    nid: str
    public_key: str
    private_key: str
    time: datetime.datetime

    class Config:
        orm_mode = True

class NodeKeyResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[NodeKey]

    class Config:
        orm_mode = True

class UserInformation(BaseModel):
    uid: str
    name: str
    full_name: str
    mail: str
    password: str
    time: datetime.datetime

    class Config:
        orm_mode = True

class UserInformationReponse(BaseModel):
    resultCode: int
    msg: str
    data: List[UserInformation]

    class Config:
        orm_mode = True

class ChangePassword(BaseModel):
    mail: str
    old_pwd: str
    new_pwd: str

    class Config:
        orm_mode = True

class ChangeMail(BaseModel):
    old_mail: str
    name: str
    password: str
    new_mail: str

    class Config:
        orm_mode = True

class UserKey(BaseModel):
    uid: str
    public_key: str
    private_key: str
    time: datetime.datetime

    class Config:
        orm_mode = True

class UserKeyResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[UserKey]

    class Config:
        orm_mode = True

class DeviceKey(BaseModel):
    did: str
    public_key: str
    private_key: str
    time: datetime.datetime

    class Config:
        orm_mode = True

class DeviceKeyResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[DeviceKey]

    class Config:
        orm_mode = True

class UserLicense(BaseModel):
    uid: str
    did: str

    class Config:
        orm_mode = True

class UserLicenseResponse(BaseModel):
    resultCode: int
    msg: str
    data: List[UserLicense]

    class Config:
        orm_mode = True

class ContentLicense(BaseModel):
    cid: str
    uid: str
    did: str

    class Config:
        orm_mode = True