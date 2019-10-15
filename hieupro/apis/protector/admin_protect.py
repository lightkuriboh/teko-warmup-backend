
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from hieupro.constants.constants import *
from functools import wraps


def admin_required(function_to_check_admin):
    @wraps(function_to_check_admin)
    def checked_admin_function(*args, **kwargs):
        payload = get_jwt_identity()
        if payload and payload['privilege'] != ADMIN_PRIVILEGE:
            return jsonify(code='fail', msg='You have to be admin to access this API')
        return function_to_check_admin(*args, **kwargs)
    return checked_admin_function
