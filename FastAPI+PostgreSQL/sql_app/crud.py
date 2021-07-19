from sqlalchemy.orm import Session
import models, schemas


# 新建内容目录表
def db_create_contentcataloglist(db: Session, contentcataloglist: schemas.ContentCatalogList):
    db_item = models.ContentCatalogList(**contentcataloglist.dict())
    db.add(db_item)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_item)  # 刷新
    return db_item

# 新建内容对象数据表
def db_create_contentobjectlocation(db: Session, contentobjectlocation: schemas.ContentObjectLocation):
    db_item = models.ContentObjectLocation(**contentobjectlocation.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 新建使用权交易表
def db_create_contentusetransaction(db: Session, contentusetransaction: schemas.ContentUseTransaction):
    db_item = models.ContentUseTransaction(**contentusetransaction.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 新建结点信息表
def db_create_nodeinformation(db: Session, nodeinformation: schemas.NodeInformation):
    db_item = models.NodeInformation(**nodeinformation.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user(db: Session, user_id: str):
    return db.query(models.ContentUseTransaction).filter(models.ContentUseTransaction.cid == user_id).first()
