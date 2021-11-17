import pytest

from mysql_orm.client import MysqlORMClient


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_orm_client.recreate_db()
        mysql_orm_client.create_first_task()
        mysql_orm_client.create_second_task()
        mysql_orm_client.create_third_task()

    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()
