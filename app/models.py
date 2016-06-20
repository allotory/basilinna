# -*- coding: utf-8 -*-

from app import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    e = db.Column(db.String(120), index = True, unique = True)

    def __init__(self, nickname=None, email=None, e=None):
        self.nickname = nickname
        self.email = email
        self.e = e

    def __repr__(self):
        return '<User %r>' % (self.nickname)