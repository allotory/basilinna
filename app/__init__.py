# -*- coding: utf-8 -*-

from flask import Flask
import app.main.csrf_token as csrf_token
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
csrf = CsrfProtect(app)

config = app.config.from_object('config')

db = SQLAlchemy(app)

# app.jinja_env.globals['csrf_token'] = csrf_token.generate_csrf_token
app.secret_key = app.config.get('SECRET_KEY')

from app import views, models