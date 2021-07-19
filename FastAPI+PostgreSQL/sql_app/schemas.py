from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    """
    请求模型验证：
    email:
    password:
    """
    password: str


class User(UserBase):
    """
    响应模型：
    id:
    email:
    is_active
    并且设置orm_mode与之兼容
    """
    id: int
    is_active: bool
    add: bool

    class Config:
        orm_mode = True


class ContentCatalogList(BaseModel):
    cid: str
    uid: str
    pid: str
    author: str
    title: str
    description: str
    publisher: str
    publishid: str
    isencrypt: str
    size: float
    content_hash: str
    state: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True

class ContentObjectLocation(BaseModel):
    cid: str
    nid1: str
    nid2: str
    nid3: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

class ContentUseTransaction(BaseModel):
    cid: str
    uid: str
    value: float
    transactionHash: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    

class NodeInformation(BaseModel):
    nid: str
    public_key: str
    node_type: int
    capacity: float
    score: int
    pid: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime