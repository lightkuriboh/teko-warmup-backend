
import pymysql.cursors
from config import DBConfig


def create_database():
    host = DBConfig.host
    user = DBConfig.username
    pwd = DBConfig.password
    db = DBConfig.db
    con = pymysql.connect(
        host=host,
        user=user,
        password=pwd,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    cursor = con.cursor()
    try:
        sql_statement = "CREATE DATABASE {}".format(db)
        cursor.execute(sql_statement)
    except:
        print('Database exists!')
