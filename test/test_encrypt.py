# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import unittest
from app.main import encryption

class TestCase(unittest.TestCase):

    # run before test
    def setUp(self):
        pass

    # run end test
    def tearDown(self):
        pass

    def test_encrypt(self):
        password = 'hahahahah'
        new_password, salt = encryption.encrypt_pass_salt(password)

        new_password2 = encryption.encrypt_pass(password, salt)

        assert new_password == new_password2

if __name__ == '__main__':
    unittest.main()