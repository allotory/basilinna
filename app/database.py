# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Ellery'

import sys
print(sys.path)

from app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# db_engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test', convert_unicode=True)
db_engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    from app import models
    Base.metadata.create_all(bind=db_engine)