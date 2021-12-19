from utils.client import TesterClient
import pytest


@pytest.fixture
def client_mysql():
    client = TesterClient()
    client.connect()
    yield client
    client.connection.close()
