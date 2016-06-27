# -*- coding: utf-8 -*-

' 校验登陆、注册时账户信息 '

__author__ = 'Ellery'

from app import db, models
from datetime import datetime

def valid_email_exist(email):
    u = models.User.query.filter_by(email=email).first()
    if u:
        return True
    else:
        return False