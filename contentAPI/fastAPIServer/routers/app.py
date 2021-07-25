# -*- coding:UTF-8 -*-
"""
Created on 2021年7月21日

@author: Xinhuiyang
应用接口
"""
import os
import sys
sys.path.append('../../')
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from contentDb import schemas
from contentDb.database import SessionLocal, engine, Base
from contentDb.crud import crudApp, crudAdmin
from globalArgs import glo
import urllib.request
import urllib.parse
import requests
from playhouse.shortcuts import model_to_dict
import time
from threading import Thread  # 导入线程函数
# from contentp2p import udp as pu
# from contentStorage import storage
# from contentStorage import storageComponent

Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建

router = APIRouter(
    tags=["app"],
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

def get_capacity():
    """Get the capacity.

    Returns:
        capacity
    """
    info = os.statvfs('/')
    free_size = info.f_bsize * info.f_bavail / 1024 / 1024
    free_size = round(free_size, 2)
    # print('可用磁盘空间:' + str(free_size) + 'MB')
    return free_size

# 内容所有权交易 -- Modifying the method of obtaining transaction hash
@router.post("/contentOwnTrade")
async def content_own_trade(cid: str, uid: str, value: float, db: Session = Depends(get_db)):
    try:
        # 1.共识存储
        data = {
            "nid": glo.get_value("ip"),
            "evidence_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "cid": cid,
            "uid": uid,
            "value": value,
            "state": 1
        }
        pu.sendJS(
            glo.get_value('udp_socket'),
            glo.get_value("leaderNid"),
            {
                "type": "requestConsensus",
                "data": data
            }
        )
        # 2.根据cid，更新PostgreSql中的uid -- 收到区块后执行区块时修改
        crudApp.modify_content_owner(db, cid, uid)
    except:
        return {'resultCode': 1,'msg': '内容所有权交易失败'}
    # 3.返回交易哈希 -- 根据交易序号获取
    while 1:
        if (glo.get_value("txHash") != "0"):
            transactionHash = glo.get_value("txHash")
        return {'resultCode': 0,'msg': '内容所有权交易成功','data': transactionHash}

# 内容使用权交易 -- Modifying the method of obtaining transaction hash
@router.post("/contentUseTrade")
async def content_use_trade(cid: str, uid: str, value: float, db: Session = Depends(get_db)):
    try:
        # 1.共识存储
        data = {
            "nid": glo.get_value("ip"),
            "evidence_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "cid": cid,
            "uid": uid,
            "value": value,
            "state": 0
        }
        pu.sendJS(
            glo.get_value('udp_socket'),
            glo.get_value("leaderNid"),
            {
                "type": "requestConsensus",
                "data": data
            }
        )
        # 2.在MySQL中存储（id、cid、uid、value、交易hash）
        item = {
            "cid": cid,
            "uid": uid,
            "value": value,
            "transactionHash": transactionHash,
            "createdAt": createdAt,
            "updatedAt": updatedAt
        }
        item = schemas.ContentUseTransaction(**item)
        crudAdmin.db_create_contentusetransaction(db=db, contentusetransaction=item)
    except:
        return {'resultCode': 1,'msg': '内容使用权交易失败'}
    # return crudAdmin.db_create_contentusetransaction(db=db, contentusetransaction=item)
    # 3.返回交易哈希-- 根据交易序号获取
    while 1:
        if (glo.get_value("txHash") != "0"):
            transactionHash = glo.get_value("txHash")
        return {'resultCode': 0,'msg': '内容使用权交易成功','data': transactionHash}

# 根结点屏蔽内容 -- Modifying the method of obtaining transaction hash
@router.post("/shiedContent")
async def shied_content(cid: str, db: Session = Depends(get_db)):
    try:
        # 1.共识存储
        data = {
            "nid": glo.get_value("ip"),
            "evidence_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "cid": cid,
            "state": 2
        }
        pu.sendJS(
            glo.get_value('udp_socket'),
            glo.get_value("leaderNid"),
            {
                "type": "requestConsensus",
                "data": data
            }
        )
        # 2.根据cid，更新PostgreSql中的status -- 收到区块后执行区块时修改
        crudApp.modify_content_status_shied(db, cid)
    except:
        return {'resultCode': 1,'msg': '根结点屏蔽内容失败'}
    # 3.返回交易哈希 -- 根据交易序号获取
    while 1:
        if (glo.get_value("txHash") != "0"):
            transactionHash = glo.get_value("txHash")
        return {'resultCode': 0,'msg': '根结点屏蔽内容成功','data': transactionHash}

# 内容发布者下架内容 -- Modifying the method of obtaining transaction hash
@router.post("/takeoffContent")
async def takeoff_content(cid: str, db: Session = Depends(get_db)):
    try:
        # 1.共识存储
        data = {
            "nid": glo.get_value("ip"),
            "evidence_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "cid": cid,
            "state": 1
        }
        pu.sendJS(
            glo.get_value('udp_socket'),
            glo.get_value("leaderNid"),
            {
                "type": "requestConsensus",
                "data": data
            }
        )
        # 2.根据cid，更新PostgreSql中的status -- 收到区块后执行区块时修改
        crudApp.modify_content_status_takeoff(db, cid)
    except:
        return {'resultCode': 1,'msg': '内容下架失败'}
    # 3.返回交易哈希 -- 根据交易序号获取
    while 1:
        if (glo.get_value("txHash") != "0"):
            transactionHash = glo.get_value("txHash")
        return {'resultCode': 0,'msg': '内容下架成功','data': transactionHash}

# 处理用户发来的内容元数据 -- 内容元数据存到哪
@router.post("/uploadContentMeta")
async def upload_contentMeta(item: schemas.ContentMeta, db: Session = Depends(get_db)):
    try:
        url='http://' + glo.get_value('ca') + ':8080/appendContent'
        result = ''
        with urllib.request.urlopen(url, item) as f:
            result = f.read().decode('utf-8')
            result = json.loads(result)
        parm = {
            "cid": result.get('cid'),
            "key": result.get('key')
        }
    except:
        return {'resultCode': 1,'msg': '内容元数据处理失败'}
    return {'resultCode': 0,'msg': '内容元数据处理成功','data': parm}

# 处理用户发来的内容对象 -- 从哪取内容元数据,文件传输
@router.post("/uploadContentObject")
async def upload_contentObject(cid: str, content: bytes, db: Session = Depends(get_db)):
    try:
        # 1.发布结点存储
        storage.storage(cid, content.file.read(), cid)
    except:
        return {'resultCode': 1,'msg': '发布结点存储内容对象失败'}
    
    # t1 = Thread(target=content_release_consensus, args=())
    # t2 = Thread(target=content_backup)
    # t1.start()
    # t2.start()
    return {'resultCode': 0,'msg': '内容发布成功','data': transactionHash}

# def content_release_consensus():
# 2.发起共识 -- return tx_hash
# def content_backup():
    # num = 0
    # 3.选备份结点
    # filePath = storageComponent.mkdir(cid)
    # filePath = filePath + os.listdir(filePath)[0]

    # fsize = os.path.getsize(filePath)
    # fsize = fsize/float(1024*1024)
    # fsize = round(fsize, 2)
    # while num < 2:
    #     nidList = storageComponent.content_node_choose(fsize)

    #     for nid in nidList:
    #         content = storage.obtain(cid)
    #         url='http://' + nid + ':5551/backupContent'
    #         data = {
    #             "cid": cid
    #         }
    #         files = {
    #             "file": content
    #         }
    #         f = requests.post(url, data=data, files=files)
    #         result = f.read().decode('utf-8')
    #         result = json.loads(result)
    #         if result.get('state') == 'true':
    #             num += 1
    # # 4.发起存储位置共识