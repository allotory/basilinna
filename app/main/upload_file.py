# -*- coding: utf-8 -*-

' 检查扩展名是否合法 '

__author__ = 'Ellery'

from app import app
import datetime, random

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')

def unique_name():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(0, 100)
    if random_num <= 10:
        random_num = str(0) + str(random_num);
    unique_num = str(now_time) + str(random_num);
    return unique_num