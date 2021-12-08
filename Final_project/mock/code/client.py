import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import VK_ID


def my_decorator(func):
    def connector(self, username):
        self.connect()
        func(self, username)
        self.connection.close()
    return connector


class MysqlORMClient:

    def __init__(self, user='test_qa1', password='qa_test1', db_name=os.environ['MOCK_DB'], host='percona', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)
        self.session = sm()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def get_vk_id(self, username):
        self.connect()
        self.session.commit()
        resp = self.session.query(VK_ID).filter_by(username=username).first()
        self.connection.close()
        return resp

    @my_decorator
    def put_vk_id(self, username):
        new_vk_id = VK_ID(
            username=username
        )
        self.session.add(new_vk_id)
        self.session.commit()