
import os
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(__file__)

_DOT_ENV_PATH = os.path.join(ROOT_PATH, '.env')
print(_DOT_ENV_PATH)
load_dotenv(_DOT_ENV_PATH)


class DBConfig:
    username = os.getenv('MYSQL_USERNAME')
    password = os.getenv('MYSQL_ROOT_PASSWORD')
    port = os.getenv('MYSQL_SERVICE_PORT')
    db = os.getenv('MYSQL_DATABASE')
    host = os.getenv('MYSQL_HOST')
    # host = os.getenv('MYSQL_HOST_WITH_DOCKER')
    host_test = os.getenv('MYSQL_HOST')
    # host_test = os.getenv('MYSQL_HOST_WITH_DOCKER')
    port_test = os.getenv('MYSQL_SERVICE_PORT')
    db_test = os.getenv('MYSQL_DATABASE_TEST')

    SQLALCHEMY_DATABASE_URI_MAIN = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        username,
        password,
        host,
        port,
        db
    )
    SQLALCHEMY_DATABASE_URI_TEST = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        username,
        password,
        host_test,
        port_test,
        db_test
    )
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_MAIN
    # SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_TEST


class JWTConfig:
    JWT_SECRET_KEY = 'super-secret-key'


class MailConfig:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'teko.email.test@gmail.com'
    MAIL_PASSWORD = 'abcxyz123!@#'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class OtherConfig:
    HOST = 'http://127.0.0.1:5000'
    CONFIRMATION_TIME_OUT = 18000
    LOGIN_TIME_OUT = 1200


class SSOServiceUsage:
    secret_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjQ3MzMwNzYsIm5iZiI6MTU2NDczM' \
                 'zA3NiwianRpIjoiNzM2MDBh' \
                 'MmUtNjU4ZS00ZTc0LWEyMmYtNDNkMzc2MjAxNWJiIiwiaWRlbnRpdHkiOnsiZG' \
                 '9tYWluIjoiMTI3LjAuMC4xIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.Lvp0CBPeLmi' \
                 'rj8ONabhJNjhXfseOubrrmSC6hOoeabQ'
