# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MYSQL_DB = 'test'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_HOST = 'localhost'
MYSQL_POST = 3306

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://%s:%s@%s:%s/%s?charset=utf8" % (MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_POST, MYSQL_DB)
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
# print(basedir)
# print(SQLALCHEMY_DATABASE_URI)