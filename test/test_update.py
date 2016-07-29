# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import unittest
from app import models, db
from app.main import db_service
from sqlalchemy import and_

class TestCase(unittest.TestCase):

    # run before test
    def setUp(self):
        pass

    # run end test
    def tearDown(self):
        pass

    def test_encrypt(self):
        # db.session.query.filter(models.Message_log.id == 8).update({models.Message_log.sender_isdel: 1})
        # models.Message_log.update().where(models.Message_log.id == 8).values(sender_isdel=1)

        message = models.Message_log.query.filter(models.Message_log.id == 8).first()
        message.sender_isdel = 0
        db_service.db_commit()

if __name__ == '__main__':
    unittest.main()