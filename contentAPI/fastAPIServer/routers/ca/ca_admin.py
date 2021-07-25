# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
管理界面接口
"""
import os
import sys
sys.path.append('../../../')
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os
from os.path import join, getsize
from contentCA.caDb import schemas
from contentCA.caDb.database import SessionLocal, engine, Base
from contentCA.caDb.crud import crudNode, crudAdmin
from globalArgs import glo
import urllib.request
import urllib.parse
import requests


Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建

router = APIRouter(
    tags=["ca_admin"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 获取内容密钥列表
@router.get("/getContentKeyList", response_model=schemas.ContentKeyReponse)
async def get_content_key_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_content_key_list(db)
    except:
        return {'resultCode': 1,'msg': '获取内容密钥列表失败','data': []}
    return {'resultCode': 0,'msg': '获取内容密钥列表成功','data': db_user}

# 获取用户列表
@router.get("/getUserList", response_model=schemas.UserInformationReponse)
async def get_user_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_user_list(db)
    except:
        return {'resultCode': 1,'msg': '获取用户列表失败','data': []}
    return {'resultCode': 0,'msg': '获取用户列表成功','data': db_user}

# 获取结点密钥列表
@router.get("/getNodeKeyList", response_model=schemas.NodeKeyResponse)
async def get_node_key_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_node_key_list(db)
    except:
        return {'resultCode': 1,'msg': '获取结点密钥列表失败','data': []}
    return {'resultCode': 0,'msg': '获取结点密钥列表成功','data': db_user}

# 获取设备密钥列表
@router.get("/getDeviceKeyList", response_model=schemas.DeviceKeyResponse)
async def get_device_key_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_device_key_list(db)
    except:
        return {'resultCode': 1,'msg': '获取设备密钥列表失败','data': []}
    return {'resultCode': 0,'msg': '获取设备密钥列表成功','data': db_user}

# 获取用户密钥列表
@router.get("/getUserKeyList", response_model=schemas.UserKeyResponse)
async def get_user_key_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_user_key_list(db)
    except:
        return {'resultCode': 1,'msg': '获取用户密钥列表失败','data': []}
    return {'resultCode': 0,'msg': '获取用户密钥列表成功','data': db_user}

# 获取设备许可列表
@router.get("/getUserDeviceList", response_model=schemas.UserLicenseResponse)
async def get_user_device_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_user_device_list(db)
    except:
        return {'resultCode': 1,'msg': '获取设备许可列表失败','data': []}
    return {'resultCode': 0,'msg': '获取设备许可列表成功','data': db_user}
