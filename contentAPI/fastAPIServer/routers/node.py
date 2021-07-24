# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
结点管理界面接口
"""
import os
import sys
sys.path.append('../../')
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os
from contentDb import schemas
from contentDb.database import SessionLocal, engine, Base
from contentDb.crud import crudNode, crudAdmin
from globalArgs import glo
import urllib.request
import urllib.parse
import requests
import random

# from contentStorage import storage

Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建

router = APIRouter(
    tags=["node"],
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

# 备份结点存储内容对象数据
@router.post("/backupContent")
async def backup_content(cid: str, content: bytes, db: Session = Depends(get_db)):
    try:
        storage.storage(cid, content.file.read(), cid)
    except:
        return {'resultCode': 1,'msg': '内容对象数据存储失败'}
    return {'resultCode': 0,'msg': '内容对象数据存储成功'}

# 更改根结点
@router.post("/changeRoot")
async def change_root(root: str, db: Session = Depends(get_db)):
    try:
        glo.set_value("root", root)
        crudNode.modify_root(db, root)
    except:
        return {'resultCode': 1,'msg': '更改根结点失败'}
    return {'resultCode': 0,'msg': '更改根结点成功'}

# 更改某个结点的结点类型
@router.post("/changeType")
async def change_type(item: schemas.changeTypeRequest, db: Session = Depends(get_db)):
    try:
        crudNode.modify_node_type(db, item.nid, item.type)
    except:
        return {'resultCode': 1,'msg': '更改结点类型失败'}
    return {'resultCode': 0,'msg': '更改结点类型成功'}

# 添加内容存储位置表
@router.post("/contentLocation", response_model=schemas.ContentObjectLocationResponse)
async def content_location(item: schemas.ContentObjectLocation, db: Session = Depends(get_db)):
    try:
       db_user = crudAdmin.db_create_contentobjectlocation(db=db, contentobjectlocation=item)
    except:
        return {'resultCode': 1,'msg': '内容存储添加失败','data': []}
    return {'resultCode': 0,'msg': '内容存储添加成功','data': [db_user]}
   
# 删除某一个结点
@router.delete("/deleteNode")
async def delete_node(nid: str, db: Session = Depends(get_db)):
    try:
        crudNode.delete_node(db, nid)
    except:
        return {'resultCode': 1,'msg': '删除结点失败'}
    return {'resultCode': 0,'msg': '删除结点成功'}

# 用户获取链接结点列表
@router.get("/getConnectionNodeList")
async def get_connection_node_list(db: Session = Depends(get_db)):
    try:
        node_list = []
        nodes = crudAdmin.get_node_list(db)
        for node in nodes:
            node_list.append(node.nid)
    except:
        return {'resultCode': 1,'msg': '获取链接结点列表失败'}
    return {'resultCode': 0,'msg': '获取链接结点列表成功', 'data': node_list}

# 用户获取内容
@router.get("/getContent")
async def get_content(cid: str, db: Session = Depends(get_db)):
    try:
        content = storage.obtain(cid)
        content = content.read()
        content = str(content, encoding = "ISO-8859-1")
    except:
        return {'resultCode': 1,'msg': '用户获取内容失败'}
    return {'resultCode': 0,'msg': '用户获取内容成功', 'data': content}

# 用户获取已购买的内容列表
@router.get("/getContentList", response_model=schemas.ContentCatalogListResponse)
async def get_content_list(uid: str, db: Session = Depends(get_db)):
    try:
        content_list = crudNode.get_user_content_list(db,uid)
    except:
        return {'resultCode': 1,'msg': '内容目录列表获取失败','data': []}
    return {'resultCode': 0,'msg': '内容目录列表获取成功','data': content_list}

# 用户根据cid获取内容结点
@router.get("/getContentNode")
async def get_content_node(cid: str, db: Session = Depends(get_db)):
    try:
        node_list = []
        # 1.根据cid从数据库中获取nid
        item = crudNode.get_content_node(db,cid)
        node_list.append(item.nid1)
        node_list.append(item.nid2)
        node_list.append(item.nid3)
        # 2.随机选取一个nid返回给用户
        nid = random.sample(node_list, 1)
    except:
        return {'resultCode': 1,'msg': '内容结点获取失败'}
    return {'resultCode': 0,'msg': '内容结点获取成功','data': nid}

# 获取最新区块状态及最新数据库状态
@router.get("/getLatestState")
async def get_latest_state(cid: str, db: Session = Depends(get_db)):
    blocks = []
    content_list = []
    location = []
    transaction_list = []
    node_list = []
    try:
        # 从数据库中获取区块列表
        db = glo.get_value("leveldb")
        height = int(db.Get("height".encode()))
        for i in range(0, height):
            block = json.loads(db.Get(str(i+1).encode()).decode())
            blocks.append(block)
            # parm[block['index']] = block
   
        # 从数据库中获取最新内容目录列表
        contents = crudAdmin.get_content_list(db)
        for content in contents:
            content_list.append(content)
        
        # 从数据库中获取最新内容存储位置表
        object_locations = crudAdmin.get_node_storage_list(db)
        for object_location in object_locations:
            location.append(object_location)

        # 从数据库中获取最新使用权交易表
        transactions = crudAdmin.get_tx_list(db)
        for transaction in transactions:
            transaction_list.append(transaction)

        # 从数据库中获取最新结点信息表
        nodes = crudAdmin.get_node_list(db)
        for node in nodes:
            node_list.append(node)

        parm = {
            "block": blocks,
            "content_list": content_list,
            "location": location,
            "transaction_list": transaction_list,
            "node_list": node_list
        }
    except:
        return {'resultCode': 1,'msg': '最新区块状态及最新数据库状态获取失败'}
    return {'resultCode': 0,'msg': '最新区块状态及最新数据库状态获取成功','data': parm}

# 更新结点的剩余存储空间大小
@router.post("/updateCapacity")
async def update_capacity(nid: str, capacity: float, db: Session = Depends(get_db)):
    try:
        crudNode.modify_node_capacity(db, nid, capacity)
    except:
        return {'resultCode': 1,'msg': '更改结点的剩余存储空间大小失败'}
    return {'resultCode': 0,'msg': '更改结点的剩余存储空间大小成功'}

# 更新内容存储位置
@router.post("/updateLocation")
async def update_location(item: schemas.updateLocationRequest, db: Session = Depends(get_db)):
    try:
        location = crudNode.get_content_node(db, item.cid)
        if location.nid1 == item.nid_previous:
            crudNode.update_location(db, item.cid, "nid1", item.nid_current)
        elif location.nid2 == item.nid_previous:
            crudNode.update_location(db, item.cid, "nid2", item.nid_current)
        else:
            crudNode.update_location(db, item.cid, "nid3", item.nid_current)
    except:
        return {'resultCode': 1,'msg': '更改内容存储位置失败'}
    return {'resultCode': 0,'msg': '更改内容存储位置成功'}



