
import unittest
from hieupro.helpers.Validation import UserValidation


class MyTestCase(unittest.TestCase):
    def test_login_format_validation(self):
        user1 = {
            'username': 'kuribohkuribohkuriboh',
            'password': 'password_mine'
        }
        self.assertEqual(UserValidation.login_format_valid(user1), False)
        user2 = {
            'username': 'kuribohkuribohkuribo',
            'password': 'password_mine'
        }
        self.assertEqual(UserValidation.login_format_valid(user2), True)
        user3 = {
            'username': 'kuribohkuribohkuribo',
            'password': '_mine'
        }
        self.assertEqual(UserValidation.login_format_valid(user3), False)

    def test_register_format_validation(self):
        user1 = {
            'username': 'kuriboh',
            'password': 'password_mine',
            'email': 'hieu.pn@teko.vn'
        }
        self.assertEqual(UserValidation.register_format_valid(user1), True)
        user2 = {
            'username': 'kuriboh',
            'password': 'password_mine',
            'email': 'hieu.pn@teko.com.vn'
        }
        self.assertEqual(UserValidation.register_format_valid(user2), True)
        user3 = {
            'username': 'kuriboh',
            'password': 'password_mine',
            'email': 'hieu.p@n@teko.com.vn'
        }
        self.assertEqual(UserValidation.register_format_valid(user3), False)
        user4 = {
            'username': 'kuriboh',
            'password': 'password_mine',
            'email': 'hieu.p@n.m@teko.com.vn'
        }
        self.assertEqual(UserValidation.register_format_valid(user4), False)

