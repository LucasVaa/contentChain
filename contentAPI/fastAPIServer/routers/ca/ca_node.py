# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
结点管理界面接口
"""
import os
import sys
import rsa
import binascii
sys.path.append('../../../')
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os
from contentCA.caDb import schemas
from contentCA.caDb.database import SessionLocal, engine, Base
from contentCA.caDb.crud import crudNode
from contentDb import schemas as schemas_node
from contentDb.database import SessionLocal as SessionLocal_node
from contentDb.database import engine as engine_node
from contentDb.database import Base as Base_node
from contentDb.crud import crudNode as crudNode_node
from contentDb.crud import crudAdmin as crudAdmin_node
from globalArgs import glo
import urllib.request
import urllib.parse
import requests
import datetime
from contentCA.generateCid import generateCid
from contentCA.generateKey import generateAES, generateNodeKey, generateEncryptAesKey, generateUserKey, generateDeviceKey


Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建
Base_node.metadata.create_all(bind=engine_node)

router = APIRouter(
    tags=["ca_node"],
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

# Dependency
def get_db_node():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = SessionLocal_node()
    try:
        yield db
    finally:
        db.close()

# 为新内容申请cid和aes密钥
@router.post("/appendContent")
async def append_content(item: schemas.ContentMeta, db: Session = Depends(get_db)):
    try:
        content_hash = item.content_hash
        result = crudNode.get_content(db, content_hash)
        if(not result):
            cid = crudNode.get_cid(db)
            cid = generateCid.generate_identity(cid)
            key = generateAES.keyGenerater(16)
            content = {
                'cid': cid,
                'content_hash': content_hash,
                'author': item.author,
                'title': item.title,
                'pid': item.pid,
                'aes_key': key,
                'time': item.createdAt
            }
            content = schemas.ContentKey(**content)
            crudNode.db_create_contentkey(db=db, contentkey=content)
        else:
            cid = result.cid
            key = result.aes_key
    except:
        return {'resultCode': 1,'msg': 'cid及密钥获取失败'}
    return {'resultCode': 0,'msg': 'cid及密钥获取成功', 'data': {'cid': cid, 'key': key}}

# 为结点申请公钥和私钥
@router.post("/appendNode")
async def append_node(nid: str, db: Session = Depends(get_db)):
    try:
        result = crudNode.get_node_by_nid(db, nid)
        if(not result):
            nodeKey = generateNodeKey.NodeKey()
            pubkey = nodeKey.pubkey
            privkey = nodeKey.privkey
            node = {
                'nid': nid,
                'public_key': pubkey,
                'private_key': privkey,
                'time': datetime.datetime.now()
            }
            node = schemas.NodeKey(**node)
            crudNode.db_create_nodekey(db=db, nodekey=node)
        else:
            pubkey = result.public_key
            privkey = result.private_key
    except:
        return {'resultCode': 1,'msg': '结点公私钥获取失败'}
    return {'resultCode': 0,'msg': '结点公私钥获取成功', 'data': {'public_key': pubkey, 'private_key': privkey}}

# 添加用户
@router.post("/appendUser")
async def append_user(item: schemas.UserInformation, db: Session = Depends(get_db)):
    try: 
        mail = item.mail
        result = crudNode.get_user_by_mail(db, mail)
        if(not result):
            uid = crudNode.get_uid(db)
            if(uid):#判断数据表是否为空
                uid = int(uid.uid) + 1
            else:
                uid = 1
            name = crudNode.get_user_by_name(db, item.name)
            if(name):#判断用户名是否存在
                return {'resultCode': 1, 'msg': '用户名已存在'}
            else:
                name = item.name
            user = {
                'uid': uid,
                'name': name,
                'full_name': item.full_name,
                'mail': mail,
                'password': item.password,
                'time': datetime.datetime.now()
            }
            user = schemas.UserInformation(**user)
            crudNode.db_create_userinformation(db=db, userinformation=user)
            return {'resultCode': 0, 'msg': '注册成功', 'data': {'uid': uid, 'name': name}}
        else:
            return {'resultCode': 1, 'msg': 'mail已注册'} 
    except:
        return {'resultCode': 1, 'msg': '注册失败'}

# 修改密码
@router.post("/changePassword")
async def change_password(item: schemas.ChangePassword, db: Session = Depends(get_db)):
    try:
        mail = item.mail
        result = crudNode.get_user_by_mail(db, mail)
        if(not result):
            return {'resultCode': 1, 'msg': 'mail不存在'}
        else:
            if(item.old_pwd == result.password):
                crudNode.update_password(db, mail, item.new_pwd)
                return {'resultCode': 0, 'msg': '密码修改成功'}
            else:
                return {'resultCode': 1, 'msg': '原密码错误'}
    except:
        return {'resultCode': 1, 'msg': '密码修改失败'}

# 邮箱验证
@router.post("/validMail")
async def valid_mail(mail: str, password: str, db: Session = Depends(get_db)):
    try:
        result = crudNode.get_user_by_mail(db, mail)
        if(not result):
            return {'resultCode': 1, 'msg': 'mail不存在'}
        else:
            if(password == result.password):
                return {'resultCode': 0, 'msg': '邮箱验证成功'}
            else:
                return {'resultCode': 1, 'msg': '密码错误'}
    except:
        return {'resultCode': 1, 'msg': '验证失败'}

# 修改邮箱
@router.post("/changeMail")
async def change_mail(item: schemas.ChangeMail, db: Session = Depends(get_db)):
    try:
        mail = item.old_mail
        result = crudNode.get_user_by_mail(db, mail)
        if(not result):
            return {'resultCode': 1, 'msg': 'mail不存在'}
        else:
            if(item.password == result.password and item.name == result.name):
                crudNode.update_mail(db, item.name, item.new_mail)
                return {'resultCode': 0, 'msg': '邮箱修改成功'}
            else:
                return {'resultCode': 1, 'msg': '密码或用户名错误'}
    except:
        return {'resultCode': 1, 'msg': '邮箱修改失败'}

# 获取内容对应的aes密钥
@router.get("/getContentKey")
async def get_content_key(cid: str, db: Session = Depends(get_db)):
    try:
        result = crudNode.get_key_by_cid(db, cid)
        if(not result):
            return {'resultCode': 1, 'msg': '该内容不存在'}
        else:
            aes_key = result.aes_key
            with open('../../contentCA/generateKey/public.pem', 'r') as f:
                pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
            aes_key = generateEncryptAesKey.encryptBookKey(pubkey, aes_key)
            aes_key = binascii.b2a_base64(aes_key).decode('utf8')
            return {'resultCode': 0, 'msg': '内容密钥获取成功', 'data': {'aeskey': aes_key}}
    except:
        return {"resultCode": 1, "message": '内容密钥获取失败'}

# 为用户申请公钥和私钥
@router.post("/getUserKey")
async def get_user_key(uid: str, db: Session = Depends(get_db)):
    try:
        result = crudNode.get_user_key_by_uid(db, uid)
        if(not result):
            userKey = generateUserKey.UserKey()
            pubkey = userKey.pubkey
            privkey = userKey.privkey
            user_key = {
                'uid': uid,
                'public_key': pubkey,
                'private_key': privkey,
                'time': datetime.datetime.now()
            }
            user_key = schemas.UserKey(**user_key)
            crudNode.db_create_userkey(db=db, userkey=user_key)
        else:
            pubkey = result.public_key
            privkey = result.private_key
    except:
        return {'resultCode': 1,'msg': '用户公私钥获取失败'}
    return {'resultCode': 0,'msg': '用户公私钥获取成功', 'data': {'public_key': pubkey, 'private_key': privkey}}

# 为设备申请公钥和私钥
@router.post("/getDeviceKey")
async def get_device_key(did: str, db: Session = Depends(get_db)):
    try:
        result = crudNode.get_device_key_by_did(db, did)
        if(not result):
            deviceKey = generateDeviceKey.DeviceKey()
            pubkey = deviceKey.pubkey
            privkey = deviceKey.privkey
            device_key = {
                'did': did,
                'public_key': pubkey,
                'private_key': privkey,
                'time': datetime.datetime.now()
            }
            device_key = schemas.DeviceKey(**device_key)
            crudNode.db_create_devicekey(db=db, devicekey=device_key)
        else:
            pubkey = result.public_key
            privkey = result.private_key
    except:
        return {'resultCode': 1,'msg': '设备公私钥获取失败'}
    return {'resultCode': 0,'msg': '设备公私钥获取成功', 'data': {'public_key': pubkey, 'private_key': privkey}}

# 获取内容许可
@router.post("/getContentLicense")
async def get_content_license(item: schemas.ContentLicense, db_node: Session = Depends(get_db_node), db: Session = Depends(get_db)):
    try:
        result = crudNode_node.get_content_license(db_node, item.cid, item.uid)
        if(not result):
            return {'resultCode': 1,'msg': '用户没有内容访问权限'}
        else:
            user_device = crudNode.get_device(db, item.uid, item.did)
            if(not user_device):
            # 判断数量
                device_num = 0
                result = crudNode.get_device_num(db, item.uid)
                for i in result:
                    device_num += 1
                if(device_num > 2):
                    return {'resultCode': 1,'msg': '设备数已达上限'}
                else:
                    user_license = {
                        'uid': item.uid,
                        'did':item.did
                    }
                    user_license = schemas.UserLicense(**user_license)
                    crudNode.db_create_userlicense(db=db, userlicense=user_license)

            aeskey = crudNode.get_key_by_cid(db, item.cid).aes_key
            device_key = crudNode.get_device_key_by_did(db, item.did)
            if(not device_key):
                deviceKey = generateDeviceKey.DeviceKey()
                pubkey = deviceKey.pubkey
                privkey = deviceKey.privkey
                device_key = {
                    'did': item.did,
                    'public_key': pubkey,
                    'private_key': privkey,
                    'time': datetime.datetime.now()
                }
                device_key = schemas.DeviceKey(**device_key)
                crudNode.db_create_devicekey(db=db, devicekey=device_key)
            else:
                pubkey = device_key.public_key

            device_pubkey = rsa.PublicKey.load_pkcs1(pubkey)
            aeskey = generateEncryptAesKey.encryptBookKey(device_pubkey, aeskey)
            aeskey = binascii.b2a_base64(aeskey).decode('utf8')
            user_pubkey = crudNode.get_user_key_by_uid(db, item.uid).public_key
            user_pubkey = rsa.PublicKey.load_pkcs1(user_pubkey)
            aeskey = generateEncryptAesKey.encryptBookKey(user_pubkey, aeskey)
            aeskey = binascii.b2a_base64(aeskey).decode('utf8')
            return {'resultCode': 0, 'msg': '内容许可获取成功', 'data': {'aeskey': aeskey}}
    except:
        return {'resultCode': 1,'msg': '内容许可获取失败'}

