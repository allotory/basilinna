# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'UsTd+_P&kv#jdQ!3Oc.Kb$yd,ey/B2i-aM8em'

SITE_NAME = 'basilinna'

MYSQL_DB = 'basilinna'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_HOST = 'localhost'
MYSQL_POST = 3306

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://%s:%s@%s:%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_POST, MYSQL_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

HOST = 'http://localhost:5000/'

UPLOAD_FOLDER = '.\\app\\static\\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# 16M
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# pagination
POSTS_PER_PAGE = 5