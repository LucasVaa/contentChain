# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
管理界面接口
"""
import os
import sys
sys.path.append('../../')
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os
from os.path import join, getsize
from contentDb import schemas
from contentDb.database import SessionLocal, engine, Base
from contentDb.crud import crudAdmin
from globalArgs import glo
import urllib.request
import urllib.parse
import requests

# from contentStorage import contentCuration

Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建

router = APIRouter(
    tags=["admin"],
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

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size / 1024 / 1024

# 添加新结点
@router.post("/addNode", response_model=schemas.NodeInformationResponse)
async def add_node(item: schemas.NodeInformation, db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.db_create_nodeinformation(db=db, nodeinformation=item)
    except:
        return {'resultCode': 1,'msg': '结点添加失败','data': []}
    return {'resultCode': 0,'msg': '结点添加成功','data': [db_user]}

# 添加新内容
@router.post("/addContent", response_model=schemas.ContentCatalogListResponse)
async def add_content(item: schemas.ContentCatalogList, db: Session = Depends(get_db)):
    try:
       db_user = crudAdmin.db_create_contentcataloglist(db=db, contentcataloglist=item)
    except:
        return {'resultCode': 1,'msg': '内容添加失败','data': []}
    return {'resultCode': 0,'msg': '内容添加成功','data': [db_user]}

# 添加新交易
@router.post("/addTx", response_model=schemas.ContentUseTransactionResponse)
async def add_tx(item: schemas.ContentUseTransaction, db: Session = Depends(get_db)):
    try:
       db_user = crudAdmin.db_create_contentusetransaction(db=db, contentusetransaction=item)
    except:
        return {'resultCode': 1,'msg': '交易添加失败','data': []}
    return {'resultCode': 0,'msg': '交易添加成功','data': [db_user]}

# 添加新内容存储
@router.post("/addLocation", response_model=schemas.ContentObjectLocationResponse)
async def add_location(item: schemas.ContentObjectLocation, db: Session = Depends(get_db)):
    try:
       db_user = crudAdmin.db_create_contentobjectlocation(db=db, contentobjectlocation=item)
    except:
        return {'resultCode': 1,'msg': '内容存储添加失败','data': []}
    return {'resultCode': 0,'msg': '内容存储添加成功','data': [db_user]}

# 获取当前网络中的结点列表信息
@router.get("/getNodeList", response_model=schemas.NodeInformationResponse)
async def get_node_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_node_list(db)
    except:
        return {'resultCode': 1,'msg': '获取结点列表信息失败','data': []}
    return {'resultCode': 0,'msg': '获取结点列表信息成功','data': db_user}

# 获取内容列表信息
@router.get("/getContentList", response_model=schemas.ContentCatalogListResponse)
async def get_content_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_content_list(db)
    except:
        return {'resultCode': 1,'msg': '获取内容列表信息失败','data': []}
    return {'resultCode': 0,'msg': '获取内容列表信息成功','data': db_user}

# 获取内容对象数据列表信息
@router.get("/getContentObjectLocationList", response_model=schemas.ContentObjectLocationResponse)
async def get_content_object_location_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_node_storage_list(db)
    except:
        return {'resultCode': 1,'msg': '获取内容对象数据列表信息失败','data': []}
    return {'resultCode': 0,'msg': '获取内容对象数据列表信息成功','data': db_user}

# 获取使用权交易列表信息
@router.get("/getTxList", response_model=schemas.ContentUseTransactionResponse)
async def get_tx_list(db: Session = Depends(get_db)):
    try:
        db_user = crudAdmin.get_tx_list(db)
    except:
        return {'resultCode': 1,'msg': '获取使用权交易列表信息失败','data': []}
    return {'resultCode': 0,'msg': '获取使用权交易列表信息成功','data': db_user}

# 更改结点的类型,并广播给全网 -- discard
@router.post("/changeType")
async def change_type(item: schemas.changeTypeRequest, db: Session = Depends(get_db)):
    try:
        glo.set_value("node_type", type)
        node_list = crudAdmin.get_node_list(db)
        for i in node_list:
            url = 'http://' + i.nid + ':5551/changeType'
            result = ''    
            with urllib.request.urlopen(url, item) as f:
                result = f.read().decode('utf-8')
                result = json.loads(result)
    except:
        return {'resultCode': 1,'msg': '广播更改结点类型失败'}
    return {'resultCode': 0,'msg': '广播更改结点类型成功'}

# 根结点删除某一个结点,并广播给全网删除 -- alter to pbft
@router.delete("/deleteNode")
async def delete_node(nid: str, db: Session = Depends(get_db)):
    try:
        node_list = crudAdmin.get_node_list(db)
        for i in node_list:
            url = 'http://' + i.nid + ':5551/deleteNode'
            result = ''    
            with urllib.request.urlopen(url, data) as f:
                result = f.read().decode('utf-8')
                result = json.loads(result)
        contentCuration.node_quit_backups(nid)
    except:
        return {'resultCode': 1,'msg': '广播删除结点失败'}
    return {'resultCode': 0,'msg': '广播删除结点成功'}

# 获取区块列表
@router.get("/getBlockList")
async def get_block_list(db: Session = Depends(get_db)):
    parm = {
        "blocks": [],
        "totalNumber": "",
        "storage": "",
    }
    try:
        db = glo.get_value("leveldb")
        height = int(db.Get("height".encode()))
        for i in range(0, height):
            block = json.loads(db.Get(str(i+1).encode()).decode())
            parm["blocks"].append(block)
            # parm[block['index']] = block
    except KeyError:
        return {'resultCode': 1,'msg': '暂无区块'}
    parm["totalNumber"] = len(parm["blocks"])
    parm["storage"] = getdirsize("/home/contentchain/consensusStorage")
    return {'resultCode': 0,'msg': parm}

# 根据nid获取结点信息
@router.get("/getNodeInfo", response_model=schemas.NodeInformationResponse)
async def get_node_info(db: Session = Depends(get_db)):
    try:
        nid = glo.get_value("ip")
        node = crudAdmin.get_node(db, nid)
    except:
        return {'resultCode': 1,'msg': '获取结点信息失败','data': []}
    return {'resultCode': 0,'msg': '获取结点成功','data': node}

# 查看某一结点发布的内容目录列表 -- Modify the judgment method of transaction
@router.get("/getNodeReleaseList", response_model=schemas.ContentCatalogListResponse)
async def get_node_release_list(nid: str, db: Session = Depends(get_db)):
    cid_list = ['1','2']
    content_list = []
    try:
        db = glo.get_value("leveldb")
        height = int(db.Get("height".encode()))
        for i in range(0, height):
            block = json.loads(db.Get(str(i+1).encode()).decode())
            for j in range(0, len(block["transactions"])):
                if len(block["transactions"][j]["data"]) == 8:
                    if block["transactions"][j]["data"]["nid"] == nid:
                        cidList.append(block["transactions"][j]["data"]["cid"])       
    except KeyError:
        return {'resultCode': 1,'msg': '暂无区块','data': []}

    # 根据cid列表获取内容
    try:
        for cid in cid_list:
            content = crudAdmin.get_content(db, cid)
            content_list.append(content)
    except:
        return {'resultCode': 1,'msg': '内容目录列表失败','data': []}
    return {'resultCode': 0,'msg': '内容目录列表成功','data': content_list}

# 查看某一结点存储的内容目录列表
@router.get("/getNodeStorageList", response_model=schemas.ContentCatalogListResponse)
async def get_node_storage_list(nid: str, db: Session = Depends(get_db)):
    # 根据nid从数据库中获取cid
    cid_list = []
    content_list = []
    try:
        contents = crudAdmin.get_cid_by_nid(db, nid)
        for content in contents:
            cid_list.append(content.cid)

        # 根据cid列表获取内容
        for cid in cid_list:
            content = crudAdmin.get_content(db, cid)
            content_list.append(content)
    except:
        return {'resultCode': 1,'msg': '内容目录列表失败','data': []}
    return {'resultCode': 0,'msg': '内容目录列表成功','data': content_list}

# 获取某一结点发起的交易 -- Modify the judgment method of transaction
@router.get("/getNodeTransactionList")
async def get_node_transaction_list(nid: str, db: Session = Depends(get_db)):
    use_transaction_list = []
    own_transaction_list = []
    try:
        db = glo.get_value("leveldb")
        height = int(db.Get("height".encode()))
        for i in range(0, height):
            block = json.loads(db.Get(str(i+1).encode()).decode())
            for j in range(0, len(block["transactions"])):
                if len(block["transactions"][j]["data"]) == 6:
                    if block["transactions"][j]["data"]["nid"] == nid:
                        if block["transactions"][j]["data"]["state"] == 0:
                            use_transaction_list.append(block["transactions"][j])
                        elif block["transactions"][j]["data"]["state"] == 1:
                            own_transaction_list.append(block["transactions"][j])
    except KeyError:
        return {'resultCode': 1,'msg': '暂无区块'}
    return {'resultCode': 0,'msg': '获取交易成功','data': {'使用权交易': use_transaction_list, '所有权交易': own_transaction_list}}

# 获取使用权和所属权交易 -- Modify the judgment method of transaction
@router.get("/getTransactionList")
async def get_transaction_list(db: Session = Depends(get_db)):
    use_transaction_list = []
    own_transaction_list = []
    try:
        db = glo.get_value("leveldb")
        height = int(db.Get("height".encode()))
        for i in range(0, height):
            block = json.loads(db.Get(str(i+1).encode()).decode())
            for j in range(0, len(block["transactions"])):
                if len(block["transactions"][j]["data"]) == 6:
                    if block["transactions"][j]["data"]["state"] == 0:
                        use_transaction_list.append(block["transactions"][j])
                    elif block["transactions"][j]["data"]["state"] == 1:
                        own_transaction_list.append(block["transactions"][j])
    except KeyError:
        return {'resultCode': 1,'msg': '暂无区块'}
    return {'resultCode': 0,'msg': '获取交易成功','data': {'使用权交易': use_transaction_list, '所有权交易': own_transaction_list}}
