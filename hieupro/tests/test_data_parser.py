
from hieupro.helpers.RecordParserBasedOnActionType import *
from hieupro.constants.constants import *

import unittest


class RecordLogin:
    random_id = 'random_id'
    username = 'username'
    success = 'success'
    logout_time = 'logout_time'


class MyTestCase(unittest.TestCase):

    def test_LOGIN(self):
        action_type = LOGIN_ACTION
        record = RecordLogin()
        new_record = parse_record_data(record, action_type)
        ok = False
        if new_record:
            ok = True
        self.assertEqual(ok, True)

    def test_LOGIN_failed(self):
        action_type = REGISTER_ACTION
        record = RecordLogin()
        self.assertRaises(AttributeError, parse_record_data, record, action_type)
