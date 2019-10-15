
import time
from sqlalchemy import and_

from hieupro.helpers.TokenServices import TokenManager
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class SSORegister(db.Model):
    __table_name__ = 'sso_register'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False, primary_key=False)
    domain = db.Column(db.VARCHAR(50), unique=False, nullable=False, primary_key=False)
    secret_key = db.Column(db.String(500), unique=False, nullable=False)
    register_time = db.Column(db.Integer, unique=False)

    @staticmethod
    def insert(domain, username):
        my_time = int(time.time())
        secret_key = TokenManager.token_provider({
            'domain': domain
        }, 0)
        new_record = SSORegister(username=username, domain=domain, secret_key=secret_key, register_time=my_time)
        db.session.add(new_record)
        db.session.commit()
        return secret_key

    @staticmethod
    def exist(domain, username):
        record = db.session.query(SSORegister).filter(
            and_(
                SSORegister.username == username,
                SSORegister.domain == domain)
        ).first()
        if record:
            return True
        return False

    @staticmethod
    def registered(secret_key):
        record = db.session.query(SSORegister).filter(SSORegister.secret_key == secret_key).first()
        if record:
            return True
        return False

    @staticmethod
    def get_domains(username):
        return db.session.query(SSORegister.domain).filter(SSORegister.username == username).all()

    @staticmethod
    def get_domain_by_secret_key(secret_key):
        record = db.session.query(SSORegister).filter(SSORegister.secret_key == secret_key).first()
        if record:
            return record.domain
        return None
