# -*- coding: utf-8 -*-

' 密码加密 '

__author__ = 'Ellery'

import hashlib
import app.main.generate_string

def encrypt_pass_salt(password):

    salt = generate_string.random_string()

    temp = (password + salt).encode('utf-8')
    new_pass = hashlib.sha256(temp).hexdigest()

    return new_pass, salt

def encrypt_pass(password, salt):
    temp = (password + salt).encode('utf-8')
    new_pass = hashlib.sha256(temp).hexdigest()

    return new_pass