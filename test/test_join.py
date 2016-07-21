# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import unittest
from app import models
from sqlalchemy import and_

class TestCase(unittest.TestCase):

    # run before test
    def setUp(self):
        pass

    # run end test
    def tearDown(self):
        pass

    def test_encrypt(self):
        #r = models.Relation.query.filter(models.Relation.member_id==1)
        # r = models.Member.query.join(models.Relation, (models.Relation.member_id == models.Member.id)).filter(models.Member.id==1).all()
        
        followees = models.Relation.query.filter(models.Relation.member_id == 1).all()
        followee_list = []
        if followees :
            for followee in followees:
                followee_info = models.Member.query.filter(models.Member.id == followee.followee_id).first()
                print(followee_info.fullname)
        #print(type(r))

if __name__ == '__main__':
    unittest.main()