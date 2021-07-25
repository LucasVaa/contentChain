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

# 添加内容使用权交易
def db_create_contentusetransaction(db: Session, contentusetransaction: schemas.ContentUseTransaction):
    db_item = models.ContentUseTransaction(**contentusetransaction.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 更改内容所属权
def db_update_uid_contentcataloglist(db: Session, contentowntrade: schemas.contentOwnTradeRequest):
    db_item = db.query(models.ContentCatalogList).filter(models.ContentCatalogList.cid == contentowntrade.cid).update({
            "uid": contentowntrade.uid,
            "updatedAt": contentowntrade.updatedAt
        })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# 下架内容和屏蔽内容
def db_update_state_contentcataloglist(db: Session, contentstate: schemas.contentStateRequest):
    db_item = db.query(models.ContentCatalogList).filter(models.ContentCatalogList.cid == contentstate.cid).update({
            "state": contentstate.state,
            "updatedAt": contentstate.updatedAt
        })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 添加内容对象存储位置数据
def db_create_contentobjectlocation(db: Session, contentobjectlocation: schemas.ContentObjectLocation):
    db_item = models.ContentObjectLocation(**contentobjectlocation.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 存储位置变更
def db_update_contentobjectlocation(db: Session, locationupdate: schemas.locationUpdateRequest):
    db_item_1 = db.query(models.ContentObjectLocation).filter(
            (models.ContentObjectLocation.cid == locationupdate.cid) &
            (models.ContentObjectLocation.nid1 == locationupdate.nid_previous)
        ).update({
            "nid1": locationupdate.nid_current,
            "updatedAt": locationupdate.updatedAt
        })
    db_item_2 = db.query(models.ContentObjectLocation).filter(
            (models.ContentObjectLocation.cid == locationupdate.cid) &
            (models.ContentObjectLocation.nid2 == locationupdate.nid_previous)
        ).update({
            "nid2": locationupdate.nid_current,
            "updatedAt": locationupdate.updatedAt
        })
    db_item_3 = db.query(models.ContentObjectLocation).filter(
            (models.ContentObjectLocation.cid == locationupdate.cid) &
            (models.ContentObjectLocation.nid3 == locationupdate.nid_previous)
        ).update({
            "nid3": locationupdate.nid_current,
            "updatedAt": locationupdate.updatedAt
        })
    db.add(db_item_1)
    db.add(db_item_2)
    db.add(db_item_3)
    db.commit()
    db.refresh(db_item_1)
    db.refresh(db_item_2)
    db.refresh(db_item_3)
    return db_item_1

# 删除某节点
def db_delete_nodeinformation(db: Session, nodedelete: schemas.nodeDeleteRequest):
    db_item = db.query(models.NodeInformation).filter(models.NodeInformation.nid == nodedelete.nid_chosen).delete()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 更改结点类型
def db_modify_mode_nodeinformation(db: Session, nodemodemodify: schemas.nodeModeModifyRequest):
    db_item = db.query(models.NodeInformation).filter(models.NodeInformation.nid == nodemodemodify.nid_chosen).update({"node_type": nodemodemodify.mode_current})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 获取当前网络中的结点列表
def get_node_list(db: Session):
    statement  = select(models.NodeInformation)
    result = db.execute(statement).scalars().all()
    nodeList = []
    for item in result:
        nodeList.append(item.nid)
    return nodeList

# 获取内容个数
def get_content_count(db: Session):
    statement  = select(models.ContentCatalogList)
    result = db.execute(statement).scalars().all()
    return len(result)

# 根据cid获取内容哈希
def get_content_hash(db: Session, cid: str):
    statement = select(models.ContentCatalogList).filter_by(cid=cid)
    result = db.execute(statement).scalars().first()
    return result.content_hash