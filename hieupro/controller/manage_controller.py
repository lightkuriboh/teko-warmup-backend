
from hieupro.models.user_actions.user_actions import UserAction
from hieupro.constants.constants import *
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.RecordParserBasedOnActionType import parse_record_data
from hieupro.models.user import User
from hieupro.models.user_actions.action import Action
from hieupro.models.user_actions.account_lock import AccountLock
from hieupro.helpers.ConstantMapper import respective_action_text_name, respective_action_model
from flask import Flask

app = Flask(__name__)


def init_reference(_app):
    global app
    app = _app


class ManageController:

    @staticmethod
    def user_delete(username):
        record = User.query_by_username(username)
        if record and record.privilege != ADMIN_PRIVILEGE:
            User.delete_by_username(username)
            return DELETE_ACCOUNT_SUCCESS
        return DELETE_ACCOUNT_FAILED_PRIVILEGE

    @staticmethod
    def user_lock(username):
        record = User.query_by_username(username)
        if record.privilege == ADMIN_PRIVILEGE:
            return LOCK_ACCOUNT_FAILED_PRIVILEGE
        if AccountLock.account_being_locked(username):
            return LOCK_ACCOUNT_FAILED_LOCKED_ALREADY
        AccountLock.lock_account(username, MyTimer.get_time())
        return LOCK_ACCOUNT_SUCCESS

    @staticmethod
    def user_unlock(username):
        if AccountLock.account_being_locked(username):
            AccountLock.unlock_account(username)
            return UNLOCK_ACCOUNT_SUCCESS
        return UNLOCK_ACCOUNT_NOT_BEING_LOCKED_FAILED

    @staticmethod
    def get_action_by_action_id(_id):
        record = UserAction.get_action_info_by_id(_id)
        if record:
            model = respective_action_model[record.action_type]
            random_id = record.action_id
            returned_record = Action.get_action_detail_by_id(random_id, model)
            # returned_record = model.get_action_detail_by_id(random_id, model)
            returned_record = parse_record_data(returned_record, record.action_type)
            return returned_record
        return None

    @staticmethod
    def user_actions(username):
        res = UserAction.get_actions_by_username(username)
        ans = []
        for row in res:
            ans.append(
                {
                    'id': row.id,
                    'time': row.time,
                    'action': respective_action_text_name[row.action_type],
                    'action_id': row.action_id
                }
            )
        return ans
