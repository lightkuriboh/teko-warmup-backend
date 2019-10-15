import time

from hieupro.controller.manage_controller import ManageController
import unittest
from hieupro.constants.constants import *
from hieupro.models.user_actions.account_lock import AccountLock


class MyTestCase(unittest.TestCase):

    def test_user_delete(self):
        self.assertEqual(ManageController.user_delete('kuriboh'), DELETE_ACCOUNT_FAILED_PRIVILEGE)

    def test_user_delete_ok(self):
        self.assertEqual(ManageController.user_delete('kuribohkuriboh'), DELETE_ACCOUNT_FAILED_PRIVILEGE)

    def test_lock_account(self):
        username = 'kuribohkute'
        AccountLock.lock_account(username, int(time.time()))
        self.assertEqual(AccountLock.account_being_locked(username), True)

    def test_unlock_account(self):
        username = 'kuribohkute'
        AccountLock.unlock_account(username)
        self.assertEqual(AccountLock.account_being_locked(username), False)

    def test_track_recorder(self):
        now = int(time.time())
        self.assertEqual(len(AccountLock.more_track(now)) > len(str(now)), True)
