import pytest

from utils.client import TesterClient

@pytest.fixture
def client_mysql():
    client = TesterClient()
    client.connect()
    yield client
    client.connection.close()