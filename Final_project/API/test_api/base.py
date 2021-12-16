import pytest

from utils.creator import Builder


class ApiBase:
    authorize = True
    publish = True
    blog_id = 378

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client_front, api_client_back, logger):
        self.api_client_front = api_client_front
        self.api_client_back = api_client_back
        self.builder = Builder()
        self.logger = logger

        if self.authorize:
            self.api_client_front.post_login()


