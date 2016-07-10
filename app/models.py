# -*- coding: utf-8 -*-

from app import db
from datetime import datetime

# 用户表
class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    email = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(256), nullable = False)
    salt = db.Column(db.String(128), nullable = False)
    create_time = db.Column(db.DateTime(), nullable = False, server_default = str(datetime.now()))
    last_login_time = db.Column(db.DateTime(), nullable = False, server_default = str(datetime.now()))
    last_login_ip = db.Column(db.String(16), nullable = False)
    status = db.Column(db.SmallInteger, nullable = False)
    remark = db.Column(db.String(256), server_default = '')
    invent = db.Column(db.String(256), nullable = False)

    def __init__(self, password, salt, email, 
                create_time, last_login_time, last_login_ip,
                status, remark, invent):
        self.email = email
        self.password = password
        self.salt = salt
        self.create_time = create_time
        self.last_login_time = last_login_time
        self.last_login_ip = last_login_ip
        self.status = status
        self.remark = remark
        self.invent = invent

    def __repr__(self):
        return '<User %r>' % (self.email)


# 用户信息表
class Member(db.Model):

    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    fullname = db.Column(db.String(64), nullable = False)
    gender = db.Column(db.Integer, nullable = False, server_default = '0')
    avatar_path = db.Column(db.String(256), server_default = '')
    location = db.Column(db.String(128), server_default = '')
    hometown = db.Column(db.String(128), server_default = '')
    description = db.Column(db.String(256), server_default = '')
    autograph = db.Column(db.String(128), server_default = '')
    personality_url = db.Column(db.String(64), server_default = '')
    is_email_actived = db.Column(db.Integer, nullable = False, server_default = '0')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # relations= db.relationship('Relation', backref='member', 
    #             lazy='dynamic')
    # blogs = db.relationship('Blog', backref='member',
    #             lazy='dynamic')
    collections = db.relationship('Collection', backref='member',
                lazy='dynamic')
    # blocks = db.relationship('Block', backref='member',
    #             lazy='dynamic')

    def __init__(self, fullname, gender, avatar_path, location, 
                hometown, description, autograph, 
                personality_url, is_email_actived, user_id):
        self.fullname = fullname
        self.gender = gender
        self.avatar_path = avatar_path
        self.location = location
        self.hometown = hometown
        self.description = description
        self.autograph = autograph
        self.personality_url = personality_url
        self.is_email_actived = is_email_actived
        self.user_id = user_id


# 用户关注表
class Relation(db.Model):

    __tablename__ = 'relation'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    followee_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    member = db.relationship('Member', foreign_keys=[member_id])
    followee = db.relationship('Member', foreign_keys=[followee_id])

    def __init__(self, member_id, followee_id):
        self.member_id = member_id
        self.followee_id = followee_id


# 微博表
class Blog(db.Model):

    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime(), nullable = False, server_default = str(datetime.now()))
    post_type = db.Column(db.String(256), nullable = False)
    via = db.Column(db.String(256), nullable = False)
    exist_pic = db.Column(db.Integer, nullable = False, server_default = '0')
    pic_path = db.Column(db.String(256), server_default = '')
    location = db.Column(db.String(256), server_default = '')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    re_from = db.Column(db.Integer, db.ForeignKey('blog.id'))
    re_member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    re_member = db.relationship('Member', foreign_keys=[re_member_id])
    member = db.relationship('Member', foreign_keys=[member_id])

    def __init__(self, content, create_time, post_type, 
                via, exist_pic, pic_path, location, member_id,
                re_from, re_member_id):
        self.content = content
        self.create_time = create_time
        self.post_type = post_type
        self.via = via
        self.exist_pic = exist_pic
        self.pic_path = pic_path
        self.location = location
        self.member_id = member_id
        self.re_from = re_from
        self.re_member_id = re_member_id


# 收藏表
class Collection(db.Model):

    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, blog_id, member_id):
        self.blog_id = blog_id
        self.member_id = member_id


# 屏蔽用户
class Block(db.Model):

    __tablename__ = 'block'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    blocked_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    blocked = db.relationship('Member', foreign_keys=[blocked_id])
    member = db.relationship('Member', foreign_keys=[member_id])
    
    def __init__(self, blocked_id, member_id):
        self.blocked_id = blocked_id
        self.member_id = member_id


# 消息内容表
class Message_text(db.Model):

    __tablename__ = 'message_text'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    content = db.Column(db.Text, nullable = False)
    message_name = db.Column(db.String(64), nullable = False)

    def __init__(self, content, message_name):
        self.content = content
        self.message_name = message_name

# 消息记录表
class Message_log(db.Model):

    __tablename__ = 'message_log'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    sender_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    text_id = db.Column(db.Integer, db.ForeignKey('message_text.id'))
    send_time = db.Column(db.DateTime(), nullable = False, server_default = str(datetime.now()))
    read_time = db.Column(db.DateTime(), nullable = False, server_default = str(datetime.now()))
    message_type = db.Column(db.String(64), nullable = False)
    sender_isdel = db.Column(db.SmallInteger, nullable = False)
    receiver_isdel = db.Column(db.SmallInteger, nullable = False)
    is_read = db.Column(db.SmallInteger, nullable = False)

    def __init__(self, sender_id, reciever_id, text_id,
            send_time, read_time, message_type, sender_isdel,
            receiver_isdel, is_read):
        self.sender_id = sender_id
        self.reciever_id = receiver_id
        self.text_id = text_id
        self.send_time = send_time
        self.read_time = read_time
        self.message_type = message_type
        self.sender_isdel = sender_isdel
        self.receiver_isdel = receiver_isdel
        self.is_read = is_read


# 兴趣爱好表
class Hobby(db.Model):

    __tablename__ = 'hobby'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    favor = db.Column(db.String(256), nullable = False)
    music = db.Column(db.String(256), nullable = False)
    movie = db.Column(db.String(256), nullable = False)
    book = db.Column(db.String(256), nullable = False)
    sport = db.Column(db.String(256), nullable = False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __inti__(self, favor, music, movie, book, sport, member_id):
        self.favor = favor
        self.music = music
        self.movie = movie
        self.book = book
        self.sport = sport


# 隐私表
class Privacy(db.Model):

    __tablename__ = 'privacy'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    allow_access = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_pm = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_findme = db.Column(db.Integer, nullable = False, server_default = '0')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, allow_access, allow_pm, allow_findme, member_id):
        self.allow_access = allow_access
        self.allow_pm = allow_pm
        self.allow_findme = allow_findme
        self.member_id = member_id


# 邮件通知表
class Emailme(db.Model):

    __tablename__ = 'emailme'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    allow_pri_msg = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_follow_me = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_new_trend = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_follow_care = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_show_follow_msg = db.Column(db.Integer, nullable = False, server_default = '0')
    allow_illegal_login = db.Column(db.Integer, nullable = False, server_default = '0')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, allow_pri_msg, allow_follow_me, allow_new_trend,
            allow_follow_care, allow_show_follow_msg, allow_illegal_login, member_id):
        self.allow_pri_msg = allow_pri_msg
        self.allow_follow_me = allow_follow_me
        self.allow_new_trend = allow_new_trend
        self.allow_follow_care = allow_follow_care
        self.allow_show_follow_msg = allow_show_follow_msg
        self.allow_illegal_login = allow_illegal_login
        self.member_id = member_id
