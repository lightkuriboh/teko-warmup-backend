

from flask_sqlalchemy import SQLAlchemy

_db = SQLAlchemy()


def init_db(my_db):
    global _db
    _db = my_db


class Kuriboh(_db.Model):
    db = _db
    __abstract__ = True

