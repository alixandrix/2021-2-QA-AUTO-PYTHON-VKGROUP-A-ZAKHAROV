import logging
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import ui.utils.creator as cr
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def login_page(driver, credentials):
    from ui.pages.login_page import LoginPage
    return LoginPage(driver=driver)


@pytest.fixture
def create_campaign(temp_dir, main_page):
    company = main_page.switcher(main_page.locators.NAVBAR_COMPANY_LOCATOR)
    company_name = cr.create_name()
    company.create_company(temp_dir, company_name)
    company.find(company.locators.CHECKER_LOCATOR)
    yield company_name
    company.delete_company(company.extract_comp_id(company_name))


@pytest.fixture
def create_segment(main_page):
    segment = main_page.switcher(main_page.locators.NAVBAR_AUDIENCE_LOCATOR)
    segment_name = cr.create_name()
    segment.create_segments(segment_name)
    yield segment_name
    segment.delete_segment(segment.extract_id(segment_name))
    segment.driver.refresh()


@pytest.fixture
def delete_segment(main_page):
    segment = main_page.switcher(main_page.locators.NAVBAR_AUDIENCE_LOCATOR)
    segment_name = cr.create_name()
    segment.create_segments(segment_name)
    segment.delete_segment(segment.extract_id(segment_name))
    segment.driver.refresh()
    yield segment_name


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


@pytest.fixture(scope='session')
def cookies(config, credentials):
    driver = get_driver(config)
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login(*credentials)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='session')
def credentials():
    with open('data.txt', 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password