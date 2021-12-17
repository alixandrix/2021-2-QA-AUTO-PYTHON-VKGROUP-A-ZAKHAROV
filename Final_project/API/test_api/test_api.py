import pytest

from API.exceptions import InvalidLoginException
from API.test_api.base import ApiBase


class TestApiAuth(ApiBase):
    authorize = False
    def test_valid_auth(self):
        self.api_client_front.post_auth(self.builder.username(), self.builder.email(), self.builder.password())
        assert 0


class TestApiLogin(ApiBase):
    def test_valid_login(self):
        self.api_client_front.post_login(self.user, self.password)
        self.api_client_front.get_logout()
        assert 0

