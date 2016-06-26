# -*- coding: utf-8 -*-

' 生成邀请链接 '

__author__ = 'Ellery'

import app.main.csrf_token as csrf_token
from app import app

def invite_url():
    link = csrf_token.random_string()
    url = app.config.get('HOST') + link
    return url