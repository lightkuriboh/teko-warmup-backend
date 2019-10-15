
from hieupro.constants.constants import *
from hieupro.helpers.MyTimer import MyTimer
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class AccountLock(db.Model):
    __table_name__ = 'locks'

    username = db.Column(db.VARCHAR(20), unique=True, nullable=False, primary_key=True)
    # time_locked = db.Column(db.Integer, unique=False, nullable=False)
    penalty = db.Column(db.Integer, unique=False, nullable=False)
    wrong_count = db.Column(db.Integer, unique=False, nullable=False)
    wrong_track = db.Column(db.VARCHAR(100), unique=False, nullable=False)

    @staticmethod
    def more_track(now):
        return "#" + str(now)

    @staticmethod
    def insert(username, _penalty, was_wrong):
        track = ''
        if was_wrong:
            track = AccountLock.more_track(MyTimer.get_time())
        record = AccountLock(username=username,
                             penalty=_penalty,
                             wrong_count=1 if was_wrong else 0,
                             wrong_track=track
                             )
        db.session.add(record)
        db.session.commit()

    @staticmethod
    def have_record(username):
        return True if db.session.query(AccountLock).filter(AccountLock.username == username).first() else False

    @staticmethod
    def lock_not_expired(penalty):
        return MyTimer.get_time() <= penalty

    @staticmethod
    def lock_account(username, current_time):
        if not AccountLock.have_record(username):
            AccountLock.insert(username, current_time + TIME_ACCOUNT_LOCK, False)
        else:
            db.session.query(AccountLock).filter(AccountLock.username == username).update({
                'wrong_count': 0,
                'penalty': current_time + TIME_ACCOUNT_LOCK,
                'wrong_track': ''
            })
            db.session.commit()

    @staticmethod
    def unlock_account(username):
        db.session.query(AccountLock).filter(AccountLock.username == username).update({
            'wrong_count': 0,
            'penalty': 0,
            'wrong_track': ''
        })
        db.session.commit()

    @staticmethod
    def failed_login(username):
        record = db.session.query(AccountLock).filter(AccountLock.username == username).first()
        if record:
            if AccountLock.lock_not_expired(record.penalty):
                return SIGNAL_ACCOUNT_LOCK
            will_wrong = 1
            will_penalty = record.penalty
            current_time = MyTimer.get_time()

            my_track = record.wrong_track.split('#')
            will_wrong_track = ''
            for track in my_track:
                if len(track) > 0 and current_time - int(track) < TIME_ACCOUNT_LOCK_DURATION:
                    will_wrong += 1
                    will_wrong_track += AccountLock.more_track(track)

            will_wrong_track += AccountLock.more_track(current_time)

            returned_code = SIGNAL_NOTHING

            if will_wrong >= LIMIT_CAPTCHA:
                returned_code = SIGNAL_CAPTCHA

            if will_wrong >= LIMIT_ACCOUNT_LOCK:
                returned_code = SIGNAL_ACCOUNT_LOCK
                AccountLock.lock_account(username, current_time)
            else:
                db.session.query(AccountLock).filter(AccountLock.username == username).update({
                    'wrong_count': will_wrong,
                    'penalty': will_penalty,
                    'wrong_track': will_wrong_track
                })
                db.session.commit()

            return returned_code
        else:
            AccountLock.insert(username, 0, True)
        return SIGNAL_NOTHING

    @staticmethod
    def account_being_locked(username):
        record = db.session.query(AccountLock).filter(AccountLock.username == username).first()
        if record:
            if AccountLock.lock_not_expired(record.penalty):
                return True
        return False
