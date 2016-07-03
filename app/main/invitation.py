# -*- coding: utf-8 -*-

' 生成邀请链接 '

__author__ = 'Ellery'

import app.main.generate_string
from app import app

def invite_url():
    link = generate_string.random_string()
    url = app.config.get('HOST') + link
    return url