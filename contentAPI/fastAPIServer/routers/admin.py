# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
主文件
"""
import os
import sys
sys.path.append('/home/lucas/Documents/content-chain/')
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from contentDb import schemas
from contentDb.database import SessionLocal, engine, Base
from contentDb.crud import crudAdmin

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


# 添加新结点
@router.post("/addNode/", response_model=schemas.NodeInformation)
async def add_node(item: schemas.NodeInformation, db: Session = Depends(get_db)):
    return crudAdmin.db_create_nodeinformation(db=db, nodeinformation=item)

# 添加新内容
@router.post("/addContent/", response_model=schemas.ContentCatalogList)
async def add_content(item: schemas.ContentCatalogList, db: Session = Depends(get_db)):
    return crudAdmin.db_create_contentcataloglist(db=db, contentcataloglist=item)

# 添加新交易
@router.post("/addTx/", response_model=schemas.ContentUseTransaction)
async def add_tx(item: schemas.ContentUseTransaction, db: Session = Depends(get_db)):
    return crudAdmin.db_create_contentusetransaction(db=db, contentusetransaction=item)

# 添加新内容存储
@router.post("/addLocation/", response_model=schemas.ContentObjectLocation)
async def add_location(item: schemas.ContentObjectLocation, db: Session = Depends(get_db)):
    return crudAdmin.db_create_contentobjectlocation(db=db, contentobjectlocation=item)

# 获取当前网络中的结点列表信息
@router.get("/getNodeList", response_model=List[schemas.NodeInformation])
async def get_node_list(db: Session = Depends(get_db)):
    db_user = crudAdmin.get_node_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Nids not found")
    return db_user

# 获取内容列表信息
@router.get("/getContentList", response_model=List[schemas.ContentCatalogList])
async def get_content_list(db: Session = Depends(get_db)):
    db_user = crudAdmin.get_content_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Contents not found")
    return db_user

# 获取内容对象数据列表信息
@router.get("/getNodeStorageList", response_model=List[schemas.ContentObjectLocation])
async def get_node_storage_list(db: Session = Depends(get_db)):
    db_user = crudAdmin.get_node_storage_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_user

# 获取使用权交易列表信息
@router.get("/getTxList", response_model=List[schemas.ContentUseTransaction])
async def get_tx_list(db: Session = Depends(get_db)):
    db_user = crudAdmin.get_tx_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Tx not found")
    return db_user

# 更改结点的类型,并广播给全网
@router.post("/changeType/")
async def change_type(nid: str, type: int, db: Session = Depends(get_db)):
    return {"nid": nid, "type": type}

# 根结点删除某一个结点,并广播给全网删除
@router.delete("/deleteNode/")
async def delete_node(nid: str, db: Session = Depends(get_db)):
    return {"nid": nid}

# 根结点删除某一个结点,并广播给全网删除
@router.get("/getBlockList/")
async def get_block_list(db: Session = Depends(get_db)):
    return {"null": "null"}

# 获取结点信息
@router.get("/getNodeInfo/")
async def get_node_info(db: Session = Depends(get_db)):
    return {"null": "null"}

# 查看某一结点发布的内容目录列表
@router.get("/getNodeReleaseList/")
async def get_node_release_list(nid: str, db: Session = Depends(get_db)):
    return {"null": "null"}

# 查看某一结点存储的内容目录列表
@router.get("/getNodeStorageList/")
async def get_node_storage_list(nid: str, db: Session = Depends(get_db)):
    return {"null": "null"}

# 获取某一结点发起的交易
@router.get("/getNodeTransactionList/")
async def get_node_transaction_list(nid: str, db: Session = Depends(get_db)):
    return {"null": "null"}

# 获取使用权和所属权交易
@router.get("/getTransactionList/")
async def get_transaction_list(db: Session = Depends(get_db)):
    return {"null": "null"}