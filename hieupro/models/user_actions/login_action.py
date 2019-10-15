
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.RandomGenerator import RandomGenerator

from config import *
from hieupro.models.user_actions.user_actions import UserAction
from hieupro.models.user_actions.action import Action
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class LoginAction(Action):
    __table_name__ = 'login_action'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    logout_time = db.Column(db.Integer, unique=False, nullable=False)
    random_id = db.Column(db.VARCHAR(30), primary_key=True, unique=False, nullable=True)
    success = db.Column(db.Boolean, unique=False)

    @staticmethod
    def update_logout(action_id):
        my_time = MyTimer.get_time()
        db.session.query(LoginAction).filter(LoginAction.random_id == action_id).update({'logout_time': my_time})
        db.session.commit()

    @staticmethod
    def insert(username, success):
        my_time = MyTimer.get_time()
        random_id = RandomGenerator.random_id()
        new_record = LoginAction(username=username, logout_time=my_time + OtherConfig.LOGIN_TIME_OUT, random_id=random_id, success=success)
        db.session.add(new_record)
        db.session.commit()
        return random_id, my_time

    @staticmethod
    def get_logout_time(username):
        action_id = UserAction.get_login_action_id_by_username(username)
        record = db.session.query(LoginAction).filter(LoginAction.random_id == action_id).first()
        if record:
            return record.logout_time
        return -1
