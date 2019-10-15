from flask_jwt_extended import decode_token

from hieupro.constants.constants import ACTION_SEND_MAIL
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.TokenServices import TokenManager
from hieupro.models.sso.sso_register import SSORegister
from hieupro.models.user import User
from hieupro.models.user_actions.login_action import LoginAction
from hieupro.task_queue.threader import MyThread
from flask import Flask
from hieupro.constants.EmailMessages import *
from hieupro.helpers.Validation import OtherValidation

app = Flask(__name__)


def init_reference(_app):
    global app
    app = _app


class SSOController:

    @staticmethod
    def sso_register(mailman, username, domain):
        if SSORegister.exist(domain=domain, username=username):
            return False
        if not OtherValidation.validate_domain(domain):
            return False
        secret_key = SSORegister.insert(domain=domain, username=username)
        email = User.get_email_by_username(username)
        my_thread = MyThread(ACTION_SEND_MAIL, app, mailman,
                             SSO_REGISTER_TITLE,
                             SSO_REGISTER_MESSAGE.format(domain, secret_key),
                             email)
        my_thread.start()
        return True

    @staticmethod
    def get_sso_information(domain, secret_key, username):
        _domain = SSORegister.get_domain_by_secret_key(secret_key)
        if not _domain:
            return None
        if _domain != domain:
            return None
        return User.get_basic_information_by_username(username=username)

    @staticmethod
    def token_is_alive(token):
        token_payload = decode_token(token)
        if TokenManager.token_expired(token_payload):
            return False
        exp = MyTimer.get_time()
        lim = LoginAction.get_logout_time(token_payload['username'])
        return exp <= lim

    @staticmethod
    def get_my_domains(username):
        return [x[0] for x in SSORegister.get_domains(username)]