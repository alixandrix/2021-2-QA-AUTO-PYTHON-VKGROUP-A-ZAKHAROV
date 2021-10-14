import pytest
from selenium import webdriver


@pytest.fixture(scope='function')
def driver():
    url = 'https://target.my.com/'
    browser = webdriver.Chrome(
            executable_path='D:\\chromedriver\\chromedriver.exe')
    browser.get(url)
    yield browser
    browser.close()