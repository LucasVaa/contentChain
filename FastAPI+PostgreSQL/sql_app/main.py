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
@app.post("/users/")
def create_user(item: schemas.ContentUseTransaction, db: Session = Depends(get_db)):
    return crud.db_create_contentusetransaction(db=db, contentusetransaction=item)


# 通过id查询用户
@app.get("/user/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    print(db_user)
    print(type(db_user))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)