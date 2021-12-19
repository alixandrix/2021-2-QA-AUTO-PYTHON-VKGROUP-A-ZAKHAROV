import allure
import pytest

from utils.creator import Builder
from API.clients.client_back import ApiClientBack

class ApiBase:
    authorize = True


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client_front, logger):
        with allure.step("Initilize api_client_front"):
            self.api_client_front = api_client_front
        self.builder = Builder()
        self.logger = logger
        if self.authorize:
            self.user = self.builder.username()
            self.email = self.builder.email()
            self.password = self.builder.password()
            with allure.step("Registration with username, password, email"):
                cookies = self.api_client_front.post_auth(self.user, self.email, self.password)
            with allure.step("Initilize api_client_back"):
                self.api_client_back = ApiClientBack(self.api_client_front.base_url, cookies)
        self.logger.info('Initial setup completed')


