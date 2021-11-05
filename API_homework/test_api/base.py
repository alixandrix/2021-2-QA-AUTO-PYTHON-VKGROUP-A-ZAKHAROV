import pytest

from utils.builder import Builder


class ApiBase:
    authorize = True
    publish = True


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, logger):
        self.api_client = api_client
        self.logger = logger
        if self.authorize:
            self.api_client.post_login()


