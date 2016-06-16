# -*- coding: utf-8 -*-

from flask import session

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = 'some_random_string()'
    return session['_csrf_token']