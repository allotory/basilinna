# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import unittest
from app import models
# from sqlalchemy import in_

class TestCase(unittest.TestCase):

    # run before test
    def setUp(self):
        pass

    # run end test
    def tearDown(self):
        pass

    def test_encrypt(self):
        followees = models.Relation.query.filter(models.Relation.member_id == 1).all()
        a = [x.followee_id for x in followees]
        a.append(1)
        print(a)
        blog_list = models.Blog.query.filter(models.Blog.member_id.in_(a)).order_by(models.Blog.id.desc()).all()
        print(len(blog_list))

if __name__ == '__main__':
    unittest.main()