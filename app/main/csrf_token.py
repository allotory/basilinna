# -*- coding: utf-8 -*-

from flask import session
import random, string

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = random_string()
    return session['_csrf_token']

def random_string():
    poolOfChars  = string.ascii_letters + string.digits
    random_codes = lambda x, y: ''.join([random.choice(x) for i in range(y)])
    return random_codes(poolOfChars, 20)