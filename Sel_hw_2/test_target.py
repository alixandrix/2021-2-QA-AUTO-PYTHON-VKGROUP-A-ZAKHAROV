import time
from urllib.parse import urlparse
from conftest import temp_dir
import pytest
from ui.fixtures import *
from base import BaseCase
from ui.pages.login_page import LoginPage
from ui.pages.company_page import CompanyPage
from ui.locators.basic_locators import LoginPageLocators


class TestInvalidAuthorization(BaseCase):
    authorize = False
    @pytest.mark.skip("SKIP")
    @pytest.mark.UI
    def test_invalid_login(self):
        login_page = LoginPage(self.driver)
        login_page.login(login='sasa60540', password='Azaza123', correct=False)
        assert login_page.find(LoginPageLocators.BAD_LOGIN_LOCATOR)

    @pytest.mark.skip("SKIP")
    @pytest.mark.UI
    def test_invalid_password(self):
        login_page = LoginPage(self.driver)
        login_page.login(login='sasa60540@gmail.com', password='Azaza228', correct=False)
        assert urlparse(self.driver.current_url).netloc == 'account.my.com'

class TestCreateCompany(BaseCase):
    @pytest.mark.UI
    def test_create_company(self, temp_dir):
        company = CompanyPage(self.driver)
        company.create_company(temp_dir)
        assert self.driver.current_url == 'https://target.my.com/dashboard#'


