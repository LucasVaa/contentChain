# -*- coding:UTF-8 -*-
"""
Created on 2021年7月21日

@author: Xinhuiyang
应用相关数据库操作
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import update
from sqlalchemy.orm import Session
from contentDb import models, schemas

# 修改内容所有者
def modify_content_owner(db: Session, cid: str, uid: str):
    db.query(models.ContentCatalogList).filter(models.ContentCatalogList.cid == cid).update({"uid": uid})
    db.commit()

# 将内容状态修改为屏蔽
def modify_content_status_shied(db: Session, cid: str):
    db.query(models.ContentCatalogList).filter(models.ContentCatalogList.cid == cid).update({"state": 2})
    db.commit()

# 将内容状态修改为下架
def modify_content_status_takeoff(db: Session, cid: str):
    db.query(models.ContentCatalogList).filter(models.ContentCatalogList.cid == cid).update({"state": 1})
    db.commit()