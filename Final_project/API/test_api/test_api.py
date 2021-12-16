import pytest

from API.exceptions import InvalidLoginException
from API.test_api.base import ApiBase


class TestApi(ApiBase):
    authorize = False

    def test_valid_login(self):
        self.api_client_front.post_registration(self.builder.username(), self.builder.email(), self.builder.password())
        assert 0

