# -*- coding: utf-8 -*-

from flask import Flask
import application.main.csrf_token as csrf_token

app = Flask(__name__)
app.config.from_object('config')

app.jinja_env.globals['csrf_token'] = csrf_token.generate_csrf_token

from application import views