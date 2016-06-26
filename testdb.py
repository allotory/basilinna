# -*- coding: utf-8 -*-

# from database import init_db
# init_db()

# from database import db_session
# from models import User
# u = User('admin', 'admin@localhost')
# db_session.add(u)
# db_session.commit()

# print(User.query.all())

# from app import db
# from app import models
# db.create_all()

import hashlib

a = "a test string".encode('utf-8')
print('md5 = %s' % (hashlib.md5(a).hexdigest()))
print('sha1 = %s' % (hashlib.sha1(a).hexdigest()))
print('sha224 = %s' % (hashlib.sha224(a).hexdigest()))
print('sha256 = %s' % (hashlib.sha256(a).hexdigest()))
print('sha384 = %s' % (hashlib.sha384(a).hexdigest()))
print('sha512 = %s' % (hashlib.sha512(a).hexdigest()))