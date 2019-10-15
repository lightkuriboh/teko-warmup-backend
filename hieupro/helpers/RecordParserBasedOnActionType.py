
from hieupro.constants.constants import *


def parse_record_data(record, action_type):
    returned_value = {
        'random_id': record.random_id,
        'username': record.username
    }

    if action_type == LOGIN_ACTION:
        returned_value['success'] = record.success
        returned_value['logout_time'] = record.logout_time

    if action_type == REGISTER_ACTION:
        returned_value['email'] = record.email
        returned_value['password'] = record.password
        returned_value['confirmation_time'] = record.confirmation_time

    if action_type == PASSWORD_CHANGE_ACTION or action_type == PASSWORD_RESET_ACTION:
        returned_value['old_password'] = record.old_password
        returned_value['new_password'] = record.new_password
        if action_type == PASSWORD_RESET_ACTION:
            returned_value['email'] = record.email
            returned_value['changed'] = record.changed

    return returned_value
