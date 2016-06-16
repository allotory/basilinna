# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Ellery'
import sys
print(sys.path)

from flask import Flask, render_template, request, session, abort
import app.main.csrf_token as csrf_token

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.jinja_env.globals['csrf_token'] = csrf_token.generate_csrf_token
 
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
        return render_template('login.html')