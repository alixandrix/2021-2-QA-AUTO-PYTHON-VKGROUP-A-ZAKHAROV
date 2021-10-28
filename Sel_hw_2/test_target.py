from urllib.parse import urlparse
import ui.utils.creator as cr
from base import BaseCase
from ui.fixtures import *
from ui.locators.basic_locators import LoginPageLocators
from ui.pages.company_page import CompanyPage
from ui.pages.login_page import LoginPage


class TestInvalidAuthorization(BaseCase):
    authorize = False

    @pytest.mark.UI
    def test_invalid_login(self):
        login_page = LoginPage(self.driver)
        login_page.login(login='sasa60540', password='Azaza123', correct=False)
        assert login_page.find(LoginPageLocators.BAD_LOGIN_LOCATOR)


    @pytest.mark.UI
    def test_invalid_password(self):
        login_page = LoginPage(self.driver)
        login_page.login(login='sasa60540@gmail.com', password='Azaza228', correct=False)
        assert urlparse(self.driver.current_url).netloc == 'account.my.com'


class TestCreateCompany(BaseCase):

    @pytest.mark.UI
    def test_create_company(self, temp_dir):
        company = self.main_page.switcher(self.main_page.locators.NAVBAR_COMPANY_LOCATOR)
        company_name = cr.create_name()
        company.create_company(temp_dir, company_name)
        company.find(company.locators.CHECKER_LOCATOR)
        assert company_name in self.driver.page_source
        company_id = company.extract_id(company_name)
        company.delete_company(company_id)


class TestSegment(BaseCase):

    @pytest.mark.UI
    def test_create_segment(self):
        segment = self.main_page.switcher(self.main_page.locators.NAVBAR_AUDIENCE_LOCATOR)
        segment_name = cr.create_name()
        segment.create_segments(segment_name)
        assert segment_name in self.driver.page_source
        segment_id = segment.extract_id(segment_name)
        segment.delete_company(segment_id)
        self.driver.refresh()

    @pytest.mark.UI
    def test_delete_segment(self):
        segment = self.main_page.switcher(self.main_page.locators.NAVBAR_AUDIENCE_LOCATOR)
        segment_name = cr.create_name()
        segment.create_segments(segment_name)
        segment_id = segment.extract_id(segment_name)
        segment.delete_company(segment_id)
        self.driver.refresh()
        assert segment_name not in self.driver.page_source





