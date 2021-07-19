from typing import List
from fastapi import FastAPI, Depends, HTTPException
import crud, schemas
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import uvicorn

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


# 新建用户
@app.post("/users/", response_model=schemas.NodeInformation)
def create_user(item: schemas.NodeInformation, db: Session = Depends(get_db)):
    return crud.db_create_nodeinformation(db=db, nodeinformation=item)


# 获取当前网络中的结点列表信息
@app.get("/get_node_list", response_model=List[schemas.NodeInformation])
def get_node_list(db: Session = Depends(get_db)):
    db_user = crud.get_node_list(db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Nids not found")
    return db_user




if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)