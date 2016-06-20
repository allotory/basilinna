# -*- coding: utf-8 -*-

from flask import Flask
import app.main.csrf_token as csrf_token
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config = app.config.from_object('config')

db = SQLAlchemy(app)

app.jinja_env.globals['csrf_token'] = csrf_token.generate_csrf_token

from app import views, models