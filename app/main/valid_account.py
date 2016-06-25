# -*- coding: utf-8 -*-

' 校验登陆、注册时账户信息 '

__author__ = 'Ellery'

from app import db, models
from datetime import datetime

def valid_email_exist(email):
    # u = models.User(email='susan@email.com', password='hahahah', salt='abc',
    #         create_time=str(datetime.now()), last_login_time=str(datetime.now()),
    #         last_login_ip='127.0.0.1', status=1, remark='haha', invent='http://hah')
    # db.session.add(u)
    # db.session.commit()

    u = models.User.query.filter_by(email=email).first()
    if u:
        return True
    else:
        return False