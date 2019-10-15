import json

import pytest
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from config import DBConfig
from hieupro.models.table_creators import TableCreators
from hieupro.controller.manage_controller import *


def bytes_to_json(my_bytes_value):
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    return data


@pytest.fixture
def app():
    app = create_app(DBConfig.SQLALCHEMY_DATABASE_URI)

    db = SQLAlchemy(app)
    table_creators = TableCreators()
    table_creators.create_all(db, uri=DBConfig.SQLALCHEMY_DATABASE_URI)
    return app


def test_example(client):
    response = client.get("/")
    data = bytes_to_json(response.data)
    assert data["msg"] == "Hello World"


def test_sso_registration(client):
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    data = {
        'query_data': {
            'domain': '127.0.0.1'
        }
    }
    response = client.post('/sso/register', data=json.dumps(data), headers=headers)
    print(bytes_to_json(response.data))
    assert response.status_code == 401


def test_sso(client):
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    data = {
        'query_data': {
            'username': 'kuriboh',
            'secret_key': 'hieupro'
        }
    }
    response = client.post('/sso/get_info', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    data = bytes_to_json(response.data)
    print(data)


def test_login(client):
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    data = {
        'query_data': {
            'username': 'kuriboh',
            'password': 'password'
        }
    }
    response = client.post('/user/login', data=json.dumps(data), headers=headers)
    assert response.status_code == 200

    data = bytes_to_json(response.data)
    assert data['code'] == 'success'
    print('token: --- ' + data['token'] + ' ---')
    print('--- ' + data["msg"] + ' ---')
    logout(client, token=data['token'])


def logout(client, token):
    mime_type = 'application/x-www-form-urlencoded'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    data = {
        'query_data': {
        }
    }
    response = client.head('/user/logout', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_register(client):
    mime_type = 'application/json'
    headers = {
        'Content-Type': mime_type,
        'Accept': mime_type
    }
    data = {
        'query_data': {
            'username': 'kuriboh',
            'password': 'password',
            'email': 'hieu.pn@teko.vn'
        }
    }
    response = client.post('/user/register', data=json.dumps(data), headers=headers)
    assert response.status_code == 200

    data = bytes_to_json(response.data)
    assert data['code'] == 'failed'
    print('--- ' + data["msg"] + ' ---')
