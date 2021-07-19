# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
主文件
"""
import os
import sys
sys.path.append(os.pardir)
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from sql_app.crud import crud_admin
from sql_app import schemas
from sql_app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建

app = FastAPI()

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
@app.post("/addNode/", response_model=schemas.NodeInformation)
def add_node(item: schemas.NodeInformation, db: Session = Depends(get_db)):
    return crud_admin.db_create_nodeinformation(db=db, nodeinformation=item)

# 添加新内容
@app.post("/addContent/", response_model=schemas.ContentCatalogList)
def add_content(item: schemas.ContentCatalogList, db: Session = Depends(get_db)):
    return crud_admin.db_create_contentcataloglist(db=db, contentcataloglist=item)

# 添加新交易
@app.post("/addTx/", response_model=schemas.ContentUseTransaction)
def add_tx(item: schemas.ContentUseTransaction, db: Session = Depends(get_db)):
    return crud_admin.db_create_contentusetransaction(db=db, contentusetransaction=item)

# 添加新内容存储
@app.post("/addLocation/", response_model=schemas.ContentObjectLocation)
def add_location(item: schemas.ContentObjectLocation, db: Session = Depends(get_db)):
    return crud_admin.db_create_contentobjectlocation(db=db, contentobjectlocation=item)

# 获取当前网络中的结点列表信息
@app.get("/getNodeList", response_model=List[schemas.NodeInformation])
def get_node_list(db: Session = Depends(get_db)):
    db_user = crud_admin.get_node_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Nids not found")
    return db_user

# 获取内容列表信息
@app.get("/getContentList", response_model=List[schemas.ContentCatalogList])
def get_content_list(db: Session = Depends(get_db)):
    db_user = crud_admin.get_content_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Contents not found")
    return db_user

# 获取内容对象数据列表信息
@app.get("/getNodeStorageList", response_model=List[schemas.ContentObjectLocation])
def get_node_storage_list(db: Session = Depends(get_db)):
    db_user = crud_admin.get_node_storage_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_user

# 获取使用权交易列表信息
@app.get("/getTxList", response_model=List[schemas.ContentUseTransaction])
def get_tx_list(db: Session = Depends(get_db)):
    db_user = crud_admin.get_tx_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Tx not found")
    return db_user
