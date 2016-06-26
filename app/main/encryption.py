# -*- coding: utf-8 -*-

' 密码加密 '

__author__ = 'Ellery'

import hashlib
import app.main.csrf_token as csrf_token

def encrypt_pass(password):

    salt = csrf_token.random_string()

    temp = (password + salt).encode('utf-8')
    new_pass = hashlib.sha256(temp).hexdigest()

    return new_pass, salt