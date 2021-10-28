import logging
import time

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators import basic_locators

CLICK_RETRY = 3
BASE_TIMEOUT = 10

#pytest -s -l -v --debug_log --alluredir=/tmp/allure -n 2
class PageNotLoadedException(Exception):
    pass


class BasePage(object):
    url = 'https://target.my.com/'
    locators = basic_locators.BasePageLocators

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('test')
        self.is_opened()


    def is_opened(self, timeout=BASE_TIMEOUT):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == self.url:
                return True

        raise PageNotLoadedException(f'{self.url} did not open in {timeout}sec for {self.__class__.__name__}.\n'
                                     f'Current url: {self.driver.current_url}.')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)


    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))


    @allure.step('Clicking on {locator}')
    def click(self, locator, timeout=None):
        self.logger.info(f'Clicking on {locator}')
        for i in range(CLICK_RETRY):
            try:
                self.find(locator, timeout=timeout)
                elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                self.scroll_to(elem)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY-1:
                    raise