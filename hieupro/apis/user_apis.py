
from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from hieupro.controller.user_controller import UserController
from hieupro.helpers.MailMan import MailMan
from hieupro.apis.protector.admin_protect import admin_required
from hieupro.apis.sso_apis import mock_get_sso_info
from config import SSOServiceUsage
from hieupro.constants.constants import *


app = Flask(__name__)
mail_man = MailMan()


def init_api(my_app):
    global app
    app = my_app
    global mail_man
    mail_man = MailMan(app)

    @app.route('/')
    def hello_world():
        return jsonify(msg="Hello World")

    @app.route('/decode_token/<path:token>')
    def decode_my_token(token):
        payload = decode_token(token)
        return jsonify(payload=payload['identity'])

    @app.route('/user', methods=["POST"])
    def test_test():
        user = request.get_json()['query_data']
        return jsonify(msg=user['username'])

    @app.route('/user/list_users')
    @jwt_required
    @admin_required
    def list_users():
        return jsonify(
            code='success',
            msg='Got all users information successfully',
            data=UserController.list_all()
        )

    @app.route('/user/list_all')
    def list_all():
        return jsonify(UserController.list_all())

    @app.route('/user/post_token', methods=['HEAD'])
    @jwt_required
    def post_token():
        return jsonify(payload=get_jwt_identity())

    @app.route('/user/logout', methods=['HEAD'])
    @jwt_required
    def logout():
        payload = get_jwt_identity()
        action_id = payload['action_id']
        UserController.logout(action_id)
        return jsonify(code='success', msg='Logged out success')

    @app.route('/user/login', methods=['POST'])
    def login():
        user = request.get_json()['query_data']
        payload = UserController.login(user)
        if payload and payload['token']:
            return jsonify(code='success', msg='Logged in successfully', token=payload['token'])
        return jsonify(code='failed', msg='username or password is incorrect', signal=payload['signal'])

    @app.route('/user/register', methods=['POST'])
    def register():
        user = request.get_json()['query_data']
        returned = UserController.register(mail_man, user, False)
        if returned == REGISTER_SUCCESS:
            return jsonify(code='success', msg='Registered successfully')
        elif returned == REGISTER_DUPLICATED_USERNAME_OR_EMAIL:
            return jsonify(code='failed', msg='username or email is duplicated')
        elif returned == REGISTER_VALIDATION_FAILED:
            return jsonify(code='failed', msg='Format validation failed')

    @app.route('/user/change_password', methods=['POST'])
    @jwt_required
    def change_password():
        user = request.get_json()['query_data']
        username = get_jwt_identity()['username']
        returned = UserController.password_change(
            username=username,
            old_password=user['password'],
            new_password=user['new_password'],
            by_admin=False
        )
        if returned == PASSWORD_CHANGE_SUCCESS:
            return jsonify(code='success', msg='Password changed successfully')
        elif returned == PASSWORD_CHANGE_FAILED:
            return jsonify(code='failed', msg='Old password is incorrect')
        elif returned == PASSWORD_CHANGE_LAST_FIVE_PASSWORDS:
            return jsonify(code='failed', msg='Duplicated with last 5 password')
        elif returned == PASSWORD_CHANGE_VALIDATION_FAILED:
            return jsonify(code='failed', msg='Provided information is invalid!')

    @app.route('/user/reset_password', methods=['POST'])
    def reset():
        user = request.get_json()['query_data']
        UserController.password_reset(mail_man, user['username'], user['email'])
        return jsonify(msg='success')

    @app.route('/user/sso_login', methods=['POST'])
    def sso_login():
        secret_key = SSOServiceUsage.secret_key
        username = request.get_json()['query_data']['username']
        resp = mock_get_sso_info({
            'username': username,
            'secret_key': secret_key
        })
        if resp:
            return jsonify(resp)
        return jsonify({})
