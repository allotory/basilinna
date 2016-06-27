# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Ellery'

from flask import Flask, render_template, request, session, abort, redirect, url_for
from app import app, models
from app.main import valid_account, encryption, invitation, db_service
from datetime import datetime
 
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

        # whether the email address is exist
        is_exist = valid_account.valid_email_exist(email)
        if is_exist:
            return render_template('signup.html', 
                error_message='该email地址已被注册',
                signup_form=request.form)
        else:
            if password != confirm_password:
                return render_template('signup.html', 
                    error_message='两次密码输入不一致',
                    signup_form=request.form)

            # encryption password
            new_password, salt = encryption.encrypt_pass_salt(password)

            # ip address
            ip = request.remote_addr

            # Invitation link
            invite_link = invitation.invite_url()

            # initial user and member db data
            u = models.User(email=email, password=new_password, salt=salt,
                create_time=str(datetime.now()), last_login_time=str(datetime.now()),
                last_login_ip=ip, status=1, remark='user', invent=invite_link)
            db_service.db_insert(u)
            db_service.db_commit()
            
            m = models.Member(fullname=nickname, gender=None, avatar_path=None,
                location=None, hometown=None, description=None, autograph=None,
                personality_url=None, is_email_actived=None, user_id=u.id)
            db_service.db_insert(m)
            db_service.db_commit()

            return redirect(url_for('login', info='注册成功，请先登录'))
    else:
        pass

@app.route('/login', methods = ['GET', 'POST'])
@app.route('/login/<info>', methods = ['GET', 'POST'])
def login(info=None):
    if request.method == 'POST':
        # do the login
        email = request.form['email']
        password = request.form['password']

        # encrypt password with salt
        u = models.User.query.filter_by(email=email).first()
        new_pass = encryption.encrypt_pass(password, u.salt)
        if u.password != new_pass:
            return render_template('login.html', error_message='邮件地址或密码错误')

        # set cookie

        # render index page with data

        # return (email + password + u.salt + u.password + new_pass)
        return render_template('index.html')
    else:
        # show the login form
        return render_template('login.html', info=info)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def server_syntax_error(error):
    return render_template('error_500.html'), 500