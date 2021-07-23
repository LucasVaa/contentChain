# -*- coding:UTF-8 -*-
"""
Created on 2021年7月21日

@author: Xinhuiyang
结点相关数据库操作
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import update,delete,or_,and_,select
from sqlalchemy.orm import Session
from contentDb import models, schemas

# 将nid为root的结点修改为根结点
def modify_root(db: Session, root: str):
    db.query(models.NodeInformation).filter(models.NodeInformation.nid == root).update({"node_type": 4})
    db.commit()

# 更改结点类型
def modify_node_type(db: Session, nid: str, node_type: int):
    db.query(models.NodeInformation).filter(models.NodeInformation.nid == nid).update({"node_type": node_type})
    db.commit()

# 删除某一结点
def delete_node(db: Session, nid: str):
    db.query(models.NodeInformation).filter(models.NodeInformation.nid == nid).delete()
    db.commit()

# 获取用户已购买的内容列表
def get_user_content_list(db: Session, uid: str):
    result = db.query(models.ContentCatalogList).join(models.ContentUseTransaction, models.ContentCatalogList.cid == models.ContentUseTransaction.cid).\
    filter(and_(or_(models.ContentCatalogList.state == 0, models.ContentCatalogList.state == 1), models.ContentUseTransaction.uid == uid)).all()
    return result

# 根据cid获取内容存储位置
def get_content_node(db: Session, cid: str):
    statement = select(models.ContentObjectLocation).filter_by(cid=cid)
    result = db.execute(statement).scalars().first()
    return result

# 更新结点的剩余存储空间大小
def modify_node_capacity(db: Session, nid: str, capacity: float):
    db.query(models.NodeInformation).filter(models.NodeInformation.nid == nid).update({"capacity": capacity})
    db.commit()

# 更新内容存储位置
def update_location(db: Session, cid: str, nid: str, nid_current: str):
    db.query(models.ContentObjectLocation).filter(models.ContentObjectLocation.cid == cid).update({nid: nid_current})
    db.commit()