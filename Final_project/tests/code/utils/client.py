import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from UI.utils.models import App_tb


class TesterClient:
    def __init__(self, user='test_qa', password='qa_test', db_name=f"{os.environ['APP_DB']}", host=os.environ['PERCONA_HOST'], port=os.environ['PERCONA_PORT']):
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

    def get_data(self, username):
        self.session.commit()
        resp = self.session.query(App_tb).filter_by(username=username).first()
        return resp

    def delete_user(self, username):
        self.session.commit()
        self.session.query(App_tb).filter_by(username=username).delete()
        self.session.commit()
