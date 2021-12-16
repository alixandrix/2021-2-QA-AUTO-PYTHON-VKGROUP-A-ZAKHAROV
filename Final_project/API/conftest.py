import pytest

from API.clients.client_front import ApiClientFront
from API.clients.client_back import ApiClientBack


@pytest.fixture
def api_client_front():
    return ApiClientFront('http://0.0.0.0:8060/')


@pytest.fixture
def api_client_back(config):
    return ApiClientBack('http://0.0.0.0:8060/')

