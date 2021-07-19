# -*- coding:UTF-8 -*-
"""
Created on 2021年7月20日

@author: WuGS
数据库配置相关
"""
import os
import sys
sys.path.append(os.pardir)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/contentchain"

# echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True
)

# SQLAlchemy中，CRUD是通过会话进行管理的，所以需要先创建会话，
# 每一个SessionLocal实例就是一个数据库session
# flush指发送到数据库语句到数据库，但数据库不一定执行写入磁盘
# commit是指提交事务，将变更保存到数据库文件中
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本映射类
Base = declarative_base()