
from validate_email import validate_email


class OtherValidation:
    @staticmethod
    def validate_domain(domain):
        return 5 < len(domain) < 21


class UserValidation:
    @staticmethod
    def check_username_valid(username):
        return 5 < len(username) < 21

    @staticmethod
    def check_password_valid(password):
        return 5 < len(password) < 51

    @staticmethod
    def check_email_valid(email):
        return 5 < len(email) < 51 and validate_email(email)

    @staticmethod
    def login_format_valid(user):
        return UserValidation.check_username_valid(user['username']) \
               and UserValidation.check_password_valid(user['password'])

    @staticmethod
    def register_format_valid(user):
        return UserValidation.check_username_valid(user['username']) \
               and UserValidation.check_password_valid(user['password']) \
               and UserValidation.check_email_valid(user['email'])

    @staticmethod
    def password_change_format_valid(payload):
        return UserValidation.check_password_valid(payload['old_password']) \
               and UserValidation.check_password_valid(payload['new_password']) \
               and UserValidation.check_username_valid(payload['username'])
