# -*- coding:UTF-8 -*-
"""
Created on 2021年7月24日

@author: Xinhuiyang
CA结点相关数据库操作
"""
import os
import sys
sys.path.append(os.pardir)
# sys.path.append('../')
from sqlalchemy import update,delete,or_,and_,select
from sqlalchemy.orm import Session
from contentCA.caDb import models, schemas


# 根据content_hash获取内容信息
def get_content(db: Session, content_hash: str):
    statement = select(models.ContentKey).filter_by(content_hash=content_hash)
    result = db.execute(statement).scalars().first()
    return result

# 添加内容密钥
def db_create_contentkey(db: Session, contentkey: schemas.ContentKey):
    db_item = models.ContentKey(**contentkey.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 获取最大cid
def get_cid(db: Session):
    result = db.query(models.ContentKey).order_by(models.ContentKey.cid.desc()).first()
    return result.cid

# 根据nid获取结点信息
def get_node_by_nid(db: Session, nid: str):
    statement = select(models.NodeKey).filter_by(nid=nid)
    result = db.execute(statement).scalars().first()
    return result

# 添加结点密钥
def db_create_nodekey(db: Session, nodekey: schemas.NodeKey):
    db_item = models.NodeKey(**nodekey.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 根据mail获取用户信息
def get_user_by_mail(db: Session, mail: str):
    statement = select(models.UserInformation).filter_by(mail=mail)
    result = db.execute(statement).scalars().first()
    return result

# 获取最大uid
def get_uid(db: Session):
    result = db.query(models.UserInformation).order_by(models.UserInformation.uid.desc()).first()
    return result

# 根据name获取用户信息
def get_user_by_name(db: Session, name: str):
    statement = select(models.UserInformation).filter_by(name=name)
    result = db.execute(statement).scalars().first()
    return result

# 添加用户信息
def db_create_userinformation(db: Session, userinformation: schemas.UserInformation):
    db_item = models.UserInformation(**userinformation.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 修改密码
def update_password(db: Session, mail: str, new_pwd: str):
    db.query(models.UserInformation).filter(models.UserInformation.mail == mail).update({"password": new_pwd})
    db.commit()

# 修改邮箱
def update_mail(db: Session, name: str, new_mail: str):
    db.query(models.UserInformation).filter(models.UserInformation.name == name).update({"mail": new_mail})
    db.commit()

# 根据cid获取内容密钥
def get_key_by_cid(db: Session, cid: str):
    statement = select(models.ContentKey).filter_by(cid=cid)
    result = db.execute(statement).scalars().first()
    return result

# 根据uid获取用户密钥信息
def get_user_key_by_uid(db: Session, uid: str):
    statement = select(models.UserKey).filter_by(uid=uid)
    result = db.execute(statement).scalars().first()
    return result

# 添加用户密钥
def db_create_userkey(db: Session, userkey: schemas.UserKey):
    db_item = models.UserKey(**userkey.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 根据did获取设备密钥信息
def get_device_key_by_did(db: Session, did: str):
    statement = select(models.DeviceKey).filter_by(did=did)
    result = db.execute(statement).scalars().first()
    return result

# 添加设备密钥
def db_create_devicekey(db: Session, devicekey: schemas.DeviceKey):
    db_item = models.DeviceKey(**devicekey.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 获取设备
def get_device(db: Session, uid: str, did: str):
    result = db.query(models.UserLicense).filter(and_(models.UserLicense.uid==uid, models.UserLicense.did==did)).first()
    return result

# 获取设备数量
def get_device_num(db: Session, uid: str):
    result = db.query(models.UserLicense).filter(models.UserLicense.uid==uid).all()
    return result

# 添加设备许可
def db_create_userlicense(db: Session, userlicense: schemas.UserLicense):
    db_item = models.UserLicense(**userlicense.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item