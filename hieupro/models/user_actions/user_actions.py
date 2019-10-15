
from sqlalchemy import and_, desc

from hieupro.constants.constants import *
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class UserAction(db.Model):
    __table_name__ = 'user_action'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False, primary_key=False)
    time = db.Column(db.Integer, unique=False, nullable=False)
    action_type = db.Column(db.Integer, unique=False, nullable=False)
    action_id = db.Column(db.VARCHAR(30), unique=False, nullable=False)
    # action_name = db.Column(db.String, unique=False, nullable=False)

    @staticmethod
    def insert(username, action_type, action_id, my_time):
        new_record = UserAction(username=username, time=my_time, action_type=action_type, action_id=action_id)
        db.session.add(new_record)
        db.session.commit()

    @staticmethod
    def get_login_action_id_by_username(username):
        record = db.session.query(UserAction).filter(
            and_(
                UserAction.username == username,
                UserAction.action_type == LOGIN_ACTION
            )
        ).first()
        if record:
            return record.action_id
        return -1

    @staticmethod
    def get_actions_by_username(username):
        records = db.session.query(UserAction).filter(UserAction.username == username).order_by(desc(UserAction.id)).limit(50).all()
        return records

    @staticmethod
    def get_action_info_by_id(_id):
        record = db.session.query(UserAction).filter(UserAction.id == _id).first()
        return record
