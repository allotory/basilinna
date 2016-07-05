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
        r = models.Relation.query.filter(and_(models.Relation.member_id==1, models.Relation.followee_id==2)).first()
        
        assert r == None

if __name__ == '__main__':
    unittest.main()