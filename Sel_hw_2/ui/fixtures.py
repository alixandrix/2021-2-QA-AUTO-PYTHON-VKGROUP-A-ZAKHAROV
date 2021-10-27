import logging
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


def get_driver(config, download_dir=None):
    browser_name = config['browser']
    if browser_name == 'chrome':
        options = Options()
        if download_dir is not None:
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})
        manager = ChromeDriverManager(version='latest', log_level=logging.CRITICAL)
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
    else:
        raise RuntimeError(f'Unsupported browser: {browser_name}')

    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver(config, temp_dir):
    url = config['url']
    with allure.step('Init browser'):
        browser = get_driver(config, download_dir=temp_dir)
        browser.get(url)

    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome'])
def all_drivers(config, request):
    url = config['url']
    config['browser'] = request.param

    browser = get_driver(config)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture(scope='session')
def cookies(config):
    driver = get_driver(config)
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login()
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

@pytest.fixture()
def file_path(self):
    return os.path.join(repo_root)
