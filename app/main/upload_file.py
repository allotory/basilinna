# -*- coding: utf-8 -*-

' 检查扩展名是否合法 '

__author__ = 'Ellery'

from app import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')