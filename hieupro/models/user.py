
from sqlalchemy import or_

from config import OtherConfig
from hieupro.helpers.TokenServices import TokenManager
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class User(db.Model):
    __table_name__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    password = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    privilege = db.Column(db.String(150), unique=False, nullable=False)

    @staticmethod
    def query_all():
        # return User.query.all()
        return db.session.query(User).all()

    @staticmethod
    def query_by_username(username):
        # return User.query.filter_by(username=username).first()
        return db.session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_email_by_username(username):
        record = db.session.query(User).filter(User.username == username).first()
        if record:
            return record.email
        return None

    @staticmethod
    def query_by_username_or_email(username, email):
        # return User.query.filter(or_(User.username == user['username'], User.email == user['email'])).first()
        return db.session.query(User).filter(or_(User.username == username, User.email == email)).first()

    @staticmethod
    def insert(new_user):
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def update_password(username, new_password):
        # User.query.filter(username=username).update({'password': new_password})
        db.session.query(User).filter(User.username == username).update({'password': new_password})
        db.session.commit()

    @staticmethod
    def get_basic_information_by_username(username):
        record = db.session.query(User).filter(User.username == username).first()
        if record:
            metadata = {
                'email': record.email,
                'username': username
            }
            token = TokenManager.token_provider(metadata, OtherConfig.LOGIN_TIME_OUT)
            return {
                'metadata': metadata,
                'token': token
            }
        return None

    @staticmethod
    def delete_by_username(username):
        db.session.query(User).filter(User.username == username).delete()
        db.session.commit()
        return True
