import pytest
from ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

CLICK_RETRY = 3
LOGIN = 'sasa60540@gmail.com'
PASSWORD = 'Azaza123'
FIO = 'Zakharov Alex Sergeevich'
TEL_NUMBER = '89001234567'


class BaseCase:

    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

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

    def fill_form(self):
        self.find(basic_locators.PROFILE_LOCATOR).click()
        fio = self.find(basic_locators.FIO_LOCATOR)
        fio.clear()
        fio.send_keys(FIO)
        tel_number = self.find(basic_locators.TEL_NUMBER_LOCATOR)
        tel_number.clear()
        tel_number.send_keys(TEL_NUMBER)
        self.find(basic_locators.BUTTON_SAVE_LOCATOR).click()
        time.sleep(1)
        self.driver.refresh()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))



