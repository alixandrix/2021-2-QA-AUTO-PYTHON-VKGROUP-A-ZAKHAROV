import os
from contextlib import contextmanager

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from UI.pages.base_page import BasePage
from UI.pages.login_page import LoginPage
from utils.creator import Builder
CLICK_RETRY = 3


class BaseCase:
    authorize = True
    driver = None
    need_login = True

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
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
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver: WebDriver = driver
        self.config = config
        self.logger = logger
        self.builder = Builder()
        self.base_page = BasePage(driver)
        self.login_page = LoginPage(driver)
        if self.authorize:
            data = request.getfixturevalue('cookies')
            cookies = data[0]
            self.user = data[1]
            self.password = data[2]
            self.email = data[3]
            if self.need_login:
                for cookie in cookies:
                    self.driver.add_cookie({'name': cookie['name'], 'value': cookie['value']})
                self.driver.refresh()
                self.main_page = request.getfixturevalue('main_page')
        self.logger.info('Initial setup completed')

    @contextmanager
    def switch_to_next_windows(self, current, close=False):
        for w in self.driver.window_handles:
            if w != current:
                self.driver.switch_to.window(w)
                break
        yield
        if close:
            self.driver.close()
        self.driver.switch_to.window(current)

        





