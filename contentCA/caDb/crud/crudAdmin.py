# -*- coding:UTF-8 -*-
"""
Created on 2021年7月24日

@author: Xinhuiyang
应用相关数据库操作
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from contentCA.caDb import models, schemas

# 获取内容密钥列表
def get_content_key_list(db: Session):
    statement  = select(models.ContentKey)
    result = db.execute(statement).scalars().all()
    return result

# 获取用户列表
def get_user_list(db: Session):
    statement  = select(models.UserInformation)
    result = db.execute(statement).scalars().all()
    return result

# 获取结点密钥列表
def get_node_key_list(db: Session):
    statement  = select(models.NodeKey)
    result = db.execute(statement).scalars().all()
    return result

# 获取设备密钥列表
def get_device_key_list(db: Session):
    statement  = select(models.DeviceKey)
    result = db.execute(statement).scalars().all()
    return result

# 获取用户密钥列表
def get_user_key_list(db: Session):
    statement  = select(models.UserKey)
    result = db.execute(statement).scalars().all()
    return result

# 获取设备许可列表
def get_user_device_list(db: Session):
    statement  = select(models.UserLicense)
    result = db.execute(statement).scalars().all()
    return result