
from flask_jwt_extended import (
    create_access_token
)
import datetime

from hieupro.helpers.MyTimer import MyTimer


class TokenManager:
    def __init__(self):
        pass

    @staticmethod
    def token_provider(payload, time_out):
        return create_access_token(identity=payload, expires_delta=datetime.timedelta(seconds=time_out))

    @staticmethod
    def token_expired(token_payload):
        exp_time = token_payload['exp']
        time_now = MyTimer.get_time()
        if time_now < exp_time:
            return False
        return True


