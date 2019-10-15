
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.RandomGenerator import RandomGenerator
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class RegisterAction(db.Model):
    __table_name__ = 'register_actions'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    random_id = db.Column(db.VARCHAR(30), primary_key=True, unique=False, nullable=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    password = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    email = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    confirmation_time = db.Column(db.Integer, unique=False, nullable=False)

    @staticmethod
    def insert(username, password, email):
        my_time = MyTimer.get_time()
        random_id = RandomGenerator.random_id()
        new_record = RegisterAction(
            random_id=random_id,
            username=username,
            password=password,
            email=email,
            confirmation_time=-1
        )
        db.session.add(new_record)
        db.session.commit()
        return random_id, my_time

    @staticmethod
    def register_confirmed(random_id):
        record = db.session.query(RegisterAction).filter(RegisterAction.random_id == random_id).first()
        print(record.confirmation_time)
        if str(record.confirmation_time) == str(-1):
            return False
        return True

    @staticmethod
    def confirm(random_id):
        my_time = MyTimer.get_time()
        db.session.query(RegisterAction).filter(RegisterAction.random_id == random_id).update(
            {'confirmation_time': my_time}
        )
        db.session.commit()