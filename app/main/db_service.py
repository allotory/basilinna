# -*- coding: utf-8 -*-

' 数据库操作 '

__author__ = 'Ellery'

from app import db, models
from datetime import datetime

def db_insert(model):
    db.session.add(model)

def db_commit():
    db.session.commit()