
from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required
from hieupro.apis.protector.admin_protect import admin_required
from hieupro.controller.manage_controller import ManageController
from hieupro.controller.user_controller import UserController
from hieupro.constants.constants import *


app = Flask(__name__)


def init_api(my_app):
    global app
    app = my_app

    @app.route('/manage/user/delete', methods=['POST'])
    @jwt_required
    @admin_required
    def delete_user():
        username = request.get_json()['query_data']['username']
        returned = ManageController.user_delete(username)
        if returned == DELETE_ACCOUNT_SUCCESS:
            return jsonify(
                code='success',
                msg='Deleted account successfully!'
            )
        elif returned == DELETE_ACCOUNT_FAILED_PRIVILEGE:
            return jsonify(
                code='failed',
                msg='Cannot delete admin account!'
            )

    @app.route('/manage/user/lock', methods=['POST'])
    @jwt_required
    @admin_required
    def lock_user():
        username = request.get_json()['query_data']['username']
        returned = ManageController.user_lock(username)
        if returned == LOCK_ACCOUNT_SUCCESS:
            return jsonify(
                code='success',
                msg='Locked account successfully!'
            )
        elif returned == LOCK_ACCOUNT_FAILED_PRIVILEGE:
            return jsonify(
                code='failed',
                msg='Cannot lock admin account!'
            )
        elif returned == LOCK_ACCOUNT_FAILED_LOCKED_ALREADY:
            return jsonify(
                code='failed',
                msg='Account locked already!'
            )

    @app.route('/manage/user/unlock', methods=['POST'])
    @jwt_required
    @admin_required
    def unlock_user():
        username = request.get_json()['query_data']['username']
        returned = ManageController.user_unlock(username)
        if returned == UNLOCK_ACCOUNT_SUCCESS:
            return jsonify(
                code='success',
                msg='Unlocked account successfully!'
            )
        elif returned == UNLOCK_ACCOUNT_NOT_BEING_LOCKED_FAILED:
            return jsonify(
                code='failed',
                msg='Account had not been locked!'
            )

    @app.route('/manage/user/modify', methods=['POST'])
    @jwt_required
    @admin_required
    def modify_user():
        payload = request.get_json()['query_data']
        username = payload['username']
        new_password = payload['new_password']
        returned = UserController.password_change(
            username=username,
            old_password=new_password,
            new_password=new_password,
            by_admin=True
        )
        if returned == PASSWORD_CHANGE_SUCCESS:
            return jsonify(
                code='success',
                msg='User information changed successfully'
            )
        elif returned == PASSWORD_CHANGE_VALIDATION_FAILED:
            print(username, new_password)
            return jsonify(
                code='failed',
                msg='Provided information is invalid!'
            )
        elif returned == PASSWORD_CHANGE_PRIVILEGE_FAILED:
            return jsonify(
                code='failed',
                msg='Your privilege is invalid for this action!'
            )

    @app.route('/manage/user/actions', methods=['POST'])
    def user_actions():
        username = request.get_json()['query_data']['username']
        return jsonify(
            code='success',
            msg='Got user\'s actions successfully!',
            data=ManageController.user_actions(username)
        )

    @app.route('/manage/user/action/detail/<path:_id>')
    @jwt_required
    @admin_required
    def action_detail(_id):
        returned = ManageController.get_action_by_action_id(_id)
        return jsonify(
            data=returned,
            msg='Getting action detail successfully!',
            code='success'
        )
