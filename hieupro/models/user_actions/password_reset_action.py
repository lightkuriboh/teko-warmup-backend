
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.RandomGenerator import RandomGenerator
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class PasswordResetAction(db.Model):
    __table_name__ = 'password_reset_actions'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    random_id = db.Column(db.VARCHAR(30), primary_key=True, unique=False, nullable=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    old_password = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    new_password = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    email = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    changed = db.Column(db.Boolean, unique=False, nullable=False)

    @staticmethod
    def insert(username, email, old_password, new_password):
        my_time = MyTimer.get_time()
        random_id = RandomGenerator.random_id()
        new_record = PasswordResetAction(
            random_id=random_id,
            username=username,
            email=email,
            old_password=old_password,
            new_password=new_password,
            changed=False
        )
        db.session.add(new_record)
        db.session.commit()
        return random_id, my_time

    @staticmethod
    def password_reset_already(random_id):
        record = db.session.query(PasswordResetAction).filter(PasswordResetAction.random_id == random_id).first()
        return record.changed

    @staticmethod
    def password_updated(random_id):
        db.session.query(PasswordResetAction).filter(PasswordResetAction.random_id == random_id).update(
            {'changed': True}
        )
        db.session.commit()
