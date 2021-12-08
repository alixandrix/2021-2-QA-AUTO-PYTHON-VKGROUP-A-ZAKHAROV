from abc import abstractmethod
from typing import Union
import pytest
from mysql_orm.client import MysqlORMClient
from utils.builder_orm import MysqlORMBuilder


class MysqlBase:

    @abstractmethod
    def prepare(self, log_file: Union[str]) -> None:
        pass


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlORMClient = mysql_orm_client
        self.mysql_builder: MysqlORMBuilder = MysqlORMBuilder(self.mysql)

        self.prepare(log_file='access.log')

    def get_task(self, schem):
        self.mysql.session.commit()
        task = self.mysql.session.query(schem)
        return task.all()
