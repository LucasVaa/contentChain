# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
应用相关数据库操作
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from contentDb import models, schemas


# 添加内容目录
def db_create_contentcataloglist(db: Session, contentcataloglist: schemas.ContentCatalogList):
    db_item = models.ContentCatalogList(**contentcataloglist.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 添加内容对象数据
def db_create_contentobjectlocation(db: Session, contentobjectlocation: schemas.ContentObjectLocation):
    db_item = models.ContentObjectLocation(**contentobjectlocation.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 添加使用权交易
def db_create_contentusetransaction(db: Session, contentusetransaction: schemas.ContentUseTransaction):
    db_item = models.ContentUseTransaction(**contentusetransaction.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 添加结点信息
def db_create_nodeinformation(db: Session, nodeinformation: schemas.NodeInformation):
    db_item = models.NodeInformation(**nodeinformation.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 获取当前网络中的结点列表信息
def get_node_list(db: Session):
    statement  = select(models.NodeInformation)
    result = db.execute(statement).scalars().all()
    return result

# 获取内容列表信息
def get_content_list(db: Session):
    statement  = select(models.ContentCatalogList)
    result = db.execute(statement).scalars().all()
    return result

# 获取使用权交易列表信息
def get_tx_list(db: Session):
    statement  = select(models.ContentUseTransaction)
    result = db.execute(statement).scalars().all()
    return result

# 获取内容对象数据列表信息
def get_node_storage_list(db: Session):
    statement  = select(models.ContentObjectLocation)
    result = db.execute(statement).scalars().all()
    return result

# 根据nid获取结点信息
def get_node(db: Session, nid: str):
    statement = select(models.NodeInformation).filter_by(nid=nid)
    result = db.execute(statement).scalars().all()
    return result

# 根据cid获取内容信息
def get_content(db: Session, cid: str):
    statement = select(models.ContentCatalogList).filter_by(cid=cid)
    result = db.execute(statement).scalars().first()
    return result

# 根据nid从数据库中获取cid
def get_cid_by_nid(db: Session, nid: str):
    result = db.query(models.ContentObjectLocation).filter(or_(models.ContentObjectLocation.nid1==nid,models.ContentObjectLocation.nid2==nid,models.ContentObjectLocation.nid3==nid)).all()
    return result