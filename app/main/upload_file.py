# -*- coding: utf-8 -*-

' 检查扩展名是否合法 '

__author__ = 'Ellery'

from app import app
import datetime, random
from PIL import Image
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')

def unique_name():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(0, 100)
    if random_num <= 10:
        random_num = str(0) + str(random_num)
    unique_num = str(now_time) + str(random_num)
    return unique_num

def image_thumbnail(filename):
    filepath = os.path.join(app.config.get('UPLOAD_FOLDER'), filename)
    im = Image.open(filepath)
    w, h = im.size

    if w > h:
        im.thumbnail((106, 106*h/w))
    else:
        im.thumbnail((106*w/h, 106))

    im.save(os.path.join(app.config.get('UPLOAD_FOLDER'), 
        os.path.splitext(filename)[0] + '_thumbnail' + os.path.splitext(filename)[1]))

def image_delete(filename):
    thumbnail_filepath = os.path.join(app.config.get('UPLOAD_FOLDER'), filename)
    filepath = thumbnail_filepath.replace('_thumbnail', '')
    os.remove(filepath)
    os.remove(thumbnail_filepath)

def cut_image(filename, box):
    filepath = os.path.join(app.config.get('UPLOAD_AVATAR_FOLDER'), filename)
    im = Image.open(filepath)
    new_im = im.crop(box)
    new_im.save(os.path.join(app.config.get('UPLOAD_AVATAR_FOLDER'), filename))