import logging
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from UI.pages.base_page import BasePage
from UI.pages.main_page import MainPage



@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)





def get_driver(config):
    browser_name = config['browser']
    selenoid = config['selenoid']
    if browser_name == 'chrome':
        options = Options()
        capabilities = {
                'browserName': 'chrome',
                'version': '96.0'
            }
        browser = webdriver.Remote(selenoid, options=options,
                                       desired_capabilities=capabilities)
    else:
        raise RuntimeError(f'Unsupported browser: {browser_name}')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    with allure.step('Init browser'):
        browser = get_driver(config)
        browser.get(url)

    yield browser
    browser.quit()





