
from config import DBConfig
from sqlalchemy import create_engine, MetaData, Table, Column


class TableCreators:

    def __init__(self):
        self.meta = MetaData()

    def create_user_table(self, db):
        users = Table('user', self.meta,
                      Column('user_id', db.Integer, primary_key=True, autoincrement=True),
                      Column('username', db.VARCHAR(20), unique=True, nullable=False),
                      Column('password', db.VARCHAR(50), unique=False, nullable=False),
                      Column('email', db.String(150), unique=True, nullable=False),
                      Column('privilege', db.String(150), unique=False, nullable=False)
                      )

    def create_login_action_table(self, db):
        login_actions = Table('login_action', self.meta,
                              Column('random_id', db.VARCHAR(30), primary_key=True, unique=False, nullable=False),
                              Column('username', db.VARCHAR(20), unique=False, nullable=False),
                              Column('logout_time', db.Integer, unique=False, nullable=False),
                              Column('success', db.Boolean, unique=False, nullable=False)
                              )

    def create_user_action_table(self, db):
        user_action = Table('user_action', self.meta,
                            Column('id', db.Integer, primary_key=True, autoincrement=True),
                            Column('username', db.VARCHAR(20), unique=False, nullable=False, primary_key=False),
                            Column('time', db.Integer, unique=False, nullable=False),
                            Column('action_type', db.Integer, unique=False, nullable=False),
                            Column('action_id', db.VARCHAR(30), unique=False, nullable=False)
                            )

    def create_register_action_table(self, db):
        register_actions = Table('register_action', self.meta,
                                 Column('random_id', db.VARCHAR(30), primary_key=True, unique=False, nullable=False),
                                 Column('username', db.VARCHAR(20), unique=False, nullable=False),
                                 Column('password', db.VARCHAR(50), unique=False, nullable=False),
                                 Column('email', db.String(150), unique=False, nullable=False),
                                 Column('confirmation_time', db.VARCHAR(30), unique=False, nullable=False)
                                 )

    def create_password_reset_action(self, db):
        password_reset_actions = Table('password_reset_action', self.meta,
                                       Column('random_id', db.VARCHAR(30), primary_key=True, unique=False, nullable=False),
                                       Column('username', db.VARCHAR(20), unique=False, nullable=False),
                                       Column('old_password', db.VARCHAR(50), unique=False, nullable=False),
                                       Column('new_password', db.VARCHAR(50), unique=False, nullable=False),
                                       Column('email', db.String(150), unique=False, nullable=False),
                                       Column('changed', db.Boolean, unique=False, nullable=False)
                                       )

    def create_password_change_action(self, db):
        password_change_actions = Table('password_change_action', self.meta,
                                        Column('random_id', db.VARCHAR(30), primary_key=True, unique=False, nullable=False),
                                        Column('username', db.VARCHAR(20), unique=False, nullable=False),
                                        Column('old_password', db.VARCHAR(50), unique=False, nullable=False),
                                        Column('new_password', db.VARCHAR(50), unique=False, nullable=False)
                                       )

    def create_account_lock_table(self, db):
        account_lock_table = Table('account_lock', self.meta,
                                   Column('username', db.VARCHAR(20), primary_key=True, unique=True, nullable=False),
                                   # Column('time_lock', db.Integer, unique=False, nullable=False),
                                   Column('penalty', db.Integer, unique=False, nullable=False),
                                   Column('wrong_count', db.Integer, unique=False, nullable=False),
                                   Column('wrong_track', db.VARCHAR(100), unique=False, nullable=False),
                           )

    def create_sso_register_table(self, db):
        sso_register_table = Table('sso_register', self.meta,
                                   Column('id', db.Integer, primary_key=True, autoincrement=True),
                                   Column('username', db.VARCHAR(20), unique=False, nullable=False),
                                   Column('domain', db.VARCHAR(50), unique=False, nullable=False),
                                   Column('secret_key', db.String(500), unique=False, nullable=False),
                                   Column('register_time', db.Integer, unique=False, nullable=False)
                                 )

    def create_all(self, db, uri=None, echo=None):
        self.create_user_table(db)
        self.create_user_action_table(db)
        self.create_account_lock_table(db)
        self.create_login_action_table(db)
        self.create_sso_register_table(db)
        self.create_register_action_table(db)
        self.create_password_reset_action(db)
        self.create_password_change_action(db)
        engine = create_engine(uri or DBConfig.SQLALCHEMY_DATABASE_URI, echo=echo or False)
        self.meta.create_all(engine)
