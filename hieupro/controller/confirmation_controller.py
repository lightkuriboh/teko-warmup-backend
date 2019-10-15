from hieupro.helpers.HashPassword import PasswordManager
from hieupro.models.user import User
from hieupro.models.user_actions.register_action import RegisterAction
from hieupro.models.user_actions.password_reset_action import PasswordResetAction
from flask import Flask

app = Flask(__name__)


def init_reference(_app):
    global app
    app = _app


class ConfirmationController:

    @staticmethod
    def confirm_register(user):
        user['password'] = PasswordManager.hashed_password(user['password'])
        my_user = User.query_by_username_or_email(user['username'], user['email'])
        if my_user:
            return False
        new_user = User(username=user['username'], password=user['password'], email=user['email'], privilege='citizen')
        if not RegisterAction.register_confirmed(user['action_id']):
            User.insert(new_user=new_user)
            RegisterAction.confirm(random_id=user['action_id'])
            return True
        return False

    @staticmethod
    def confirm_password_reset(payload):
        payload['new_password'] = PasswordManager.hashed_password(payload['new_password'])
        if not PasswordResetAction.password_reset_already(payload['action_id']):
            User.update_password(username=payload['username'], new_password=payload['new_password'])
            PasswordResetAction.password_updated(random_id=payload['action_id'])
            return True
        return False
