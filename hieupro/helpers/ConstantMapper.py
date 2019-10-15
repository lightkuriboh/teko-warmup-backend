
from hieupro.models.user_actions.login_action import LoginAction
from hieupro.models.user_actions.password_change_action import PasswordChangeAction
from hieupro.models.user_actions.password_reset_action import PasswordResetAction
from hieupro.models.user_actions.register_action import RegisterAction
from hieupro.constants.constants import *

respective_action_model = {
    LOGIN_ACTION: LoginAction,
    PASSWORD_CHANGE_ACTION: PasswordChangeAction,
    PASSWORD_RESET_ACTION: PasswordResetAction,
    REGISTER_ACTION: RegisterAction
}


respective_action_text_name = {
    REGISTER_ACTION: 'REGISTER',
    LOGIN_ACTION: 'LOGIN',
    PASSWORD_CHANGE_ACTION: 'PASSWORD_CHANGE',
    PASSWORD_RESET_ACTION: 'PASSWORD_RESET'
}