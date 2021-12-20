import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.creator import Builder
from utils.client import TesterClient
from UI.pages.base_page import BasePage
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def client_mysql():
    client = TesterClient()
    client.connect()
    yield client
    client.connection.close()

@pytest.fixture
def main_page(driver):
    from UI.pages.main_page import MainPage
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

@pytest.fixture(scope='session')
def registration(base_page):
    auth_page = base_page.switch()
    user = Builder.username()
    password = Builder.password()
    main_p = auth_page.register(user, password, Builder.email())
    main_p.find(main_p.locators.LOGOUT_LOCATOR)
    return user, password



@pytest.fixture(scope='session')
def cookies(config):
    driver: WebDriver = get_driver(config)
    driver.get(config['url'])
    base_page = BasePage(driver)
    auth_page = base_page.switch()
    user = Builder.username(username_length=10)
    password = Builder.password()
    email = Builder.email()
    main_p = auth_page.register(user, password, email)
    main_p.find(main_p.locators.LOGOUT_LOCATOR)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies, user, password, email




