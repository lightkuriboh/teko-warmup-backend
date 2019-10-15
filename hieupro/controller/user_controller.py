from flask import Flask

from config import OtherConfig
from hieupro.models.user import User
from hieupro.models.user_actions.account_lock import AccountLock
from hieupro.models.user_actions.user_actions import UserAction
from hieupro.models.user_actions.login_action import LoginAction
from hieupro.models.user_actions.register_action import RegisterAction
from hieupro.models.user_actions.password_reset_action import PasswordResetAction
from hieupro.models.user_actions.password_change_action import PasswordChangeAction
from hieupro.constants.constants import *
from hieupro.constants.EmailMessages import *

from hieupro.helpers.RandomGenerator import RandomGenerator
from hieupro.helpers.TokenServices import TokenManager
from hieupro.helpers.HashPassword import PasswordManager
from hieupro.task_queue.threader import MyThread
from hieupro.helpers.Validation import UserValidation

app = Flask(__name__)


def init_reference(_app):
    global app
    app = _app


class UserController:

    @staticmethod
    def list_all():
        res = User.query_all()
        ans = []
        for row in res:
            ans.append({'username': row.username,
                        'password': row.password,
                        'email': row.email,
                        'privilege': row.privilege,
                        'is_locked': AccountLock.account_being_locked(row.username)
                        })
        return ans

    @staticmethod
    def register(mailman, user, by_admin):
        if not UserValidation.register_format_valid(user):
            return REGISTER_VALIDATION_FAILED
        user['password'] = PasswordManager.hashed_password(user['password'])
        my_user = User.query_by_username_or_email(user['username'], user['email'])
        if my_user:
            return REGISTER_DUPLICATED_USERNAME_OR_EMAIL
        random_id, my_time = RegisterAction.insert(user['username'], user['password'], user['email'])
        UserAction.insert(user['username'], REGISTER_ACTION, random_id, my_time)
        token_register = TokenManager.token_provider({
            'username': user['username'],
            'password': user['password'],
            'email': user['email'],
            'action_id': random_id
        }, OtherConfig.CONFIRMATION_TIME_OUT)
        my_thread = MyThread(ACTION_SEND_MAIL, app, mailman, REGISTER_TITLE,
                             REGISTER_MESSAGE + OtherConfig.HOST + '/confirm/register/' + str(token_register),
                             user['email'])
        my_thread.start()
        return REGISTER_SUCCESS

    @staticmethod
    def login_action(username):
        random_id, my_time = LoginAction.insert(username=username, success=True)
        UserAction.insert(username=username, action_type=LOGIN_ACTION, action_id=random_id, my_time=my_time)
        return random_id

    @staticmethod
    def login(user):
        if not UserValidation.login_format_valid(user):
            return None
        username = user['username']
        password = user['password']
        password = PasswordManager.hashed_password(password)
        my_user = User.query_by_username(username=username)
        returned_value = {
            'signal': SIGNAL_NOTHING,
            'token': None
        }
        if my_user:
            if my_user.password == password:
                random_id = UserController.login_action(my_user.username)
                if not AccountLock.account_being_locked(username):
                    AccountLock.unlock_account(username)
                    return {
                        'signal': SIGNAL_NOTHING,
                        'token': TokenManager.token_provider(
                            {
                                'username': my_user.username,
                                'privilege': my_user.privilege,
                                'action_id': random_id
                            },
                            OtherConfig.LOGIN_TIME_OUT
                        )
                    }
                else:
                    return {
                        'signal': SIGNAL_ACCOUNT_LOCK,
                        'token': None
                    }
            else:
                returned_value['signal'] = AccountLock.failed_login(username)
        random_id, my_time = LoginAction.insert(username=username, success=False)
        UserAction.insert(username=username, action_type=LOGIN_ACTION, action_id=random_id, my_time=my_time)

        return returned_value

    @staticmethod
    def logout(action_id):
        LoginAction.update_logout(action_id)

    @staticmethod
    def password_change(username, old_password, new_password, by_admin):
        if not UserValidation.password_change_format_valid({
            'username': username,
            'old_password': old_password,
            'new_password': new_password
        }):
            return PASSWORD_CHANGE_VALIDATION_FAILED
        old_password = PasswordManager.hashed_password(old_password)
        new_password = PasswordManager.hashed_password(new_password)
        verify_user = User.query_by_username(username=username)
        if verify_user:
            if by_admin and verify_user.privilege == ADMIN_PRIVILEGE:
                return PASSWORD_CHANGE_PRIVILEGE_FAILED
            if by_admin or verify_user.password == old_password:
                last_five_password = PasswordChangeAction.last_five_password(username)
                if not by_admin and new_password in last_five_password:
                    return PASSWORD_CHANGE_LAST_FIVE_PASSWORDS
                old_password = verify_user.password
                User.update_password(username=username, new_password=new_password)
                random_id, my_time = PasswordChangeAction.insert(
                    username=username,
                    old_password=old_password,
                    new_password=new_password
                )
                UserAction.insert(username=username, action_type=PASSWORD_CHANGE_ACTION, action_id=random_id, my_time=my_time)
                return PASSWORD_CHANGE_SUCCESS
        return PASSWORD_CHANGE_FAILED

    @staticmethod
    def password_reset(mailman, username, email=None):
        my_user = User.query_by_username(username)
        old_password = my_user.password
        right_email = my_user.email
        if right_email != email:
            return
        new_random_password = RandomGenerator.random_password()
        random_id, my_time = PasswordResetAction.insert(
            username=username,
            email=email,
            old_password=old_password,
            new_password=new_random_password
        )
        UserAction.insert(username=username, action_type=PASSWORD_RESET_ACTION, action_id=random_id, my_time=my_time)
        token_password_reset = TokenManager.token_provider({
            'username': username,
            'new_password': new_random_password,
            'action_id': random_id
        }, OtherConfig.CONFIRMATION_TIME_OUT)
        my_thread = MyThread(ACTION_SEND_MAIL, app, mailman, PASSWORD_RESET_TITLE,
                             'username: {}\npassword: {}\n'.format(username, new_random_password)
                             + PASSWORD_RESET_MESSAGE
                             + OtherConfig.HOST + '/confirm/password_reset/' + str(token_password_reset),
                             email)
        my_thread.start()
        return token_password_reset
        # my_thread.join()
