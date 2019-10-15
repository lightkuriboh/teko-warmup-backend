
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from flask_sqlalchemy import SQLAlchemy
from config import DBConfig
from hieupro.apis import user_apis, confirm_apis, sso_apis, manage_apis
from hieupro.controller import user_controller, sso_controller, manage_controller, confirmation_controller

from hieupro.db.database_creator import create_database
from hieupro.models.table_creators import TableCreators
from hieupro.models import kuriboh
from hieupro.config.configure_app import configure_app
# from hieupro.task_queue.task_mail import MyCelery


def create_app(db_uri):
    _app = Flask(__name__)
    configure_app(_app, db_uri)
    CORS(_app)
    JWTManager(_app)
    user_apis.init_api(_app)
    confirm_apis.init_api(_app)
    sso_apis.init_api(_app)
    manage_apis.init_api(_app)
    return _app


def init_models(_db):
    kuriboh.init_db(_db)


create_database()

app = create_app(DBConfig.SQLALCHEMY_DATABASE_URI)

db = SQLAlchemy(app)
init_models(db)
table_creators = TableCreators()
table_creators.create_all(db, uri=DBConfig.SQLALCHEMY_DATABASE_URI, echo=True)

confirmation_controller.init_reference(app)
user_controller.init_reference(app)
sso_controller.init_reference(app)
manage_controller.init_reference(app)

print('dfnifhguierhtuierhtuierhsuitheruihtertuiheruithuwieuithwe')


if __name__ == '__main__':
    app.run(debug=True)
