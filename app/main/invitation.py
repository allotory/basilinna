# -*- coding: utf-8 -*-

' 生成邀请链接 '

__author__ = 'Ellery'

import app.main.generate_string as generate

def invite_url():
    link = generate.random_string()
    return link