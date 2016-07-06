# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import unittest
from app import models
from app.main import db_service
from sqlalchemy import func

class TestCase(unittest.TestCase):

    # run before test
    def setUp(self):
        pass

    # run end test
    def tearDown(self):
        pass

    def test_encrypt(self):
        # following_count = models.Relation.query(models.Relation.member_id, func.count('*').label('following_count')).filter_by(member_id=1).all()
        # following_count = models.Relation.query(models.Relation.member_id).count().filter_by(member_id=1)
        # following_count = models.Relation.query(func.count(models.Relation.member_id).label('average')).filter(models.Relation.member_id==1)
        following_count = models.Relation.query.filter(models.Relation.member_id == 1).count()
        print(following_count)

if __name__ == '__main__':
    unittest.main()