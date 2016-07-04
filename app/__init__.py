# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
csrf = CsrfProtect(app)

config = app.config.from_object('config')

db = SQLAlchemy(app)

app.secret_key = app.config.get('SECRET_KEY')

from app import views, models