# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Ellery'

from flask import Flask, render_template, request, session, abort
from app import app
 
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

@app.route('/', methods=['GET'])
def index():
    return render_template('space.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # do the login
        username = request.form['email']
        password = request.form['password']
        print(username)
        print(password)
        print('haha')
        return render_template('index.html')
    else:
        # show the login form
        from app.database import init_db
        init_db()
        return render_template('login.html')