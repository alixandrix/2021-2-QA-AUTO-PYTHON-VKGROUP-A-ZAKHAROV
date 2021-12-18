import pytest

from API.clients.client_front import ApiClientFront



@pytest.fixture
def api_client_front():
    return ApiClientFront('http://0.0.0.0:8060/')



