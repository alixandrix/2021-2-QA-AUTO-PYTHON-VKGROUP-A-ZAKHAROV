import allure
import pytest

from utils.creator import Builder


class ApiBase:
    authorize = True


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client_front, api_client_back, logger):
        self.api_client_front = api_client_front
        self.api_client_back = api_client_back
        self.builder = Builder()
        self.logger = logger
        if self.authorize:
            self.user = self.builder.username()
            self.email = self.builder.email()
            self.password = self.builder.password()
            with allure.step("Registration with username, password, email"):
                self.api_client_front.post_auth(self.user, self.email, self.password)
        self.logger.info('Initial setup completed')


