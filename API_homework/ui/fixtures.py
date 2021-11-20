import uuid
import pytest


@pytest.fixture
def create_name():
    return str(uuid.uuid4())
