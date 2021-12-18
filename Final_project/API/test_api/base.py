import os

import allure
import pytest

from utils.creator import Builder
from API.clients.client_back import ApiClientBack

class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def api_report(self, driver, request, temp_dir):
        failed_tests_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_tests_count:
            screenshot = os.path.join(temp_dir, 'failure.png')
            driver.get_screenshot_as_file(screenshot)
            allure.attach.file(screenshot, 'failure.png', attachment_type=allure.attachment_type.PNG)

            browser_log = os.path.join(temp_dir, 'browser.log')
            with open(browser_log, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")

            with open(browser_log, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

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


