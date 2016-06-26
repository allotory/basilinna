# -*- coding: utf-8 -*-

' 数据库操作 '

__author__ = 'Ellery'

from app import db, models
from datetime import datetime

def insert_user(user):
    # u = models.User(email='susan@email.com', password='hahahah', salt='abc',
    #         create_time=str(datetime.now()), last_login_time=str(datetime.now()),
    #         last_login_ip='127.0.0.1', status=1, remark='haha', invent='http://hah')
    db.session.add(user)
    db.session.commit()
