# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Ellery'

from flask import Flask, render_template, request, session, abort
from app import app
from app.main import valid_account
 
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

@app.route('/', methods=['GET'])
def index():
    return render_template('space.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # show the signup form
        return render_template('signup.html')
    elif request.method == 'POST':
        # do the signup
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        valid_account.valid_email_exist(email)
        return email
        # return render_template('index.html')
    else:
        pass

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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def server_syntax_error(error):
    return render_template('error_500.html'), 500