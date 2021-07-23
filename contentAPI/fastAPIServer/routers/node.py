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
    if storage.storage(cid, content.file.read(), cid):
        return {"state": 'true'}
    return {"state": 'false'}

# 更改根结点 -- 修改返回结果
@router.post("/changeRoot")
async def change_root(root: str, db: Session = Depends(get_db)):
    glo.set_value("root", root)
    crudNode.modify_root(db, root)
    return 'true'

# 更改某个结点的结点类型 -- 修改返回结果
@router.post("/changeType")
async def change_type(item: schemas.changeTypeRequest, db: Session = Depends(get_db)):
    crudNode.modify_node_type(db, item.nid, item.type)
    return 'true'

# 添加内容存储位置表 -- 修改返回结果
@router.post("/contentLocation", response_model=schemas.ContentObjectLocation)
async def content_location(item: schemas.ContentObjectLocation, db: Session = Depends(get_db)):
    return crudAdmin.db_create_contentobjectlocation(db=db, contentobjectlocation=item)
   
# 删除某一个结点 -- 修改返回结果
@router.delete("/deleteNode")
async def delete_node(nid: str, db: Session = Depends(get_db)):
    crudNode.delete_node(db, nid)
    return 'true'

# 用户获取链接结点列表
@router.get("/getConnectionNodeList")
async def get_connection_node_list(db: Session = Depends(get_db)):
    try:
        node_list = []
        nodes = crudAdmin.get_node_list(db)
        for node in nodes:
            node_list.append(node.nid)
        return node_list
    except:
        print("数据插入出错")
        return [json.dumps({"resultCode": -1, "uid": uid, "name": name, "message": "数据库出错"}).encode("utf-8")]

# 用户获取内容
@router.get("/getContent")
async def get_content(cid: str, db: Session = Depends(get_db)):
    content = storage.obtain(cid)
    content = content.read()
    content = str(content, encoding = "ISO-8859-1")
    return content

# 用户获取已购买的内容列表
@router.get("/getContentList", response_model=List[schemas.ContentCatalogList])
async def get_content_list(uid: str, db: Session = Depends(get_db)):
    content_list = crudNode.get_user_content_list(db,uid)
    return content_list

# 用户根据cid获取内容结点
@router.get("/getContentNode")
async def get_content_node(cid: str, db: Session = Depends(get_db)):
    node_list = []
    # 1.根据cid从数据库中获取nid
    item = crudNode.get_content_node(db,cid)
    node_list.append(item.nid1)
    node_list.append(item.nid2)
    node_list.append(item.nid3)
    # 2.随机选取一个nid返回给用户
    nid = random.sample(node_list, 1)
    return nid

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
    except Exception as e:
        print('Catch a Exception', e)
   
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
    return parm

# 更新结点的剩余存储空间大小 -- 修改返回结果
@router.post("/updateCapacity")
async def update_capacity(nid: str, capacity: float, db: Session = Depends(get_db)):
    crudNode.modify_node_capacity(db, nid, capacity)
    return 'true'

# 更新内容存储位置 -- 修改返回结果
@router.post("/updateLocation")
async def update_location(item: schemas.updateLocationRequest, db: Session = Depends(get_db)):
    location = crudNode.get_content_node(db, item.cid)
    if location.nid1 == item.nid_previous:
        crudNode.update_location(db, item.cid, "nid1", item.nid_current)
    elif location.nid2 == item.nid_previous:
        crudNode.update_location(db, item.cid, "nid2", item.nid_current)
    else:
        crudNode.update_location(db, item.cid, "nid3", item.nid_current)
    return 'true'



