
from hieupro.helpers.MyTimer import MyTimer
from hieupro.helpers.RandomGenerator import RandomGenerator
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class PasswordChangeAction(db.Model):
    __table_name__ = 'password_change_actions'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    random_id = db.Column(db.VARCHAR(30), primary_key=True, unique=False, nullable=True)
    username = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    old_password = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    new_password = db.Column(db.VARCHAR(50), unique=False, nullable=False)

    @staticmethod
    def insert(username, old_password, new_password):
        my_time = MyTimer.get_time()
        random_id = RandomGenerator.random_id()
        new_record = PasswordChangeAction(
            random_id=random_id,
            username=username,
            old_password=old_password,
            new_password=new_password
        )
        db.session.add(new_record)
        db.session.commit()
        return random_id, my_time

    @staticmethod
    def last_five_password(username):
        last_five_record = db.session.query(PasswordChangeAction).filter(PasswordChangeAction.username == username)\
            .order_by(PasswordChangeAction.random_id.desc()).limit(5).all()
        result = []
        for record in last_five_record:
            result.append(record.new_password)
        return result
