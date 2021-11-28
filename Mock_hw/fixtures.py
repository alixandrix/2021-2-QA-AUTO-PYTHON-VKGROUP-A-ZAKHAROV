import pytest
from client.client import Client
from settings import MOCK_PORT, MOCK_HOST
from faker import Faker

fake = Faker()


@pytest.fixture
def surname():
    return fake.last_name()


@pytest.fixture
def name():
    return fake.first_name()


@pytest.fixture
def client():
    some_client = Client(MOCK_HOST, MOCK_PORT)
    some_client.connect()
    return some_client
