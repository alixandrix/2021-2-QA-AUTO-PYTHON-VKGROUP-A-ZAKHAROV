import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.creator import Builder
from utils.client import TesterClient


@pytest.fixture
def base_page(driver):
    from pages.base_page import BasePage
    return BasePage(driver=driver)


@pytest.fixture
def client_mysql():
    client = TesterClient()
    client.connect()
    yield client
    client.connection.close()


@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage
    return MainPage(driver=driver)


@pytest.fixture
def registr_page(driver):
    from pages.registr_page import RegistrationPage
    return RegistrationPage(driver=driver)


@pytest.fixture
def topic():
    form_data = Builder().registration_form()
    return form_data




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





