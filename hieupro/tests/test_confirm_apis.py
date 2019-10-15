import pytest
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from config import DBConfig
from hieupro.helpers.MailMan import MailMan
from hieupro.models.table_creators import TableCreators
from hieupro.controller.user_controller import UserController
import json

mail_man = MailMan()


@pytest.fixture
def app():
    app = create_app(DBConfig.SQLALCHEMY_DATABASE_URI)

    db = SQLAlchemy(app)
    table_creators = TableCreators()
    table_creators.create_all(db, uri=DBConfig.SQLALCHEMY_DATABASE_URI)
    global mail_man
    mail_man = MailMan(app)
    return app


def test_example(client):
    response = client.get("/confirm/password_reset/token")
    assert response.status_code == 422


def test_reset(client):
    token = UserController.password_reset(mail_man, 'kuribohkute', 'hieu.pn@teko.vn')
    assert len(token) > 0
    response = client.get("/confirm/password_reset/{}".format(token))
    assert response.status_code == 200
