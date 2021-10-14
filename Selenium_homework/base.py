import pytest
from ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

CLICK_RETRY = 3
LOGIN = 'sasa60540@gmail.com'
PASSWORD = 'Azaza123'


class BaseCase:

    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def search(self, query):
        search = self.find(basic_locators.QUERY_LOCATOR)
        search.send_keys(query)
        go_button = self.find(basic_locators.GO_LOCATOR)
        go_button.click()

    def login(self):
        enter_butt = self.find(basic_locators.ENTER1_LOCATOR)
        enter_butt.click()
        login = self.find(basic_locators.LOGIN_LOCATOR)
        login.clear()
        login.send_keys(LOGIN)
        passw = self.find(basic_locators.PASSW_LOCATOR)
        passw.clear()
        passw.send_keys(PASSWORD)
        enter = self.find(basic_locators.ENTER2_LOCATOR)
        enter.click()


    def logout(self):
        exit_first_butt = self.find(basic_locators.INF_BUTT)
        exit_first_butt.click()
        time.sleep(4)
        self.find(basic_locators.EXIT_LOCATOR).click()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator, timeout=timeout)
                elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise