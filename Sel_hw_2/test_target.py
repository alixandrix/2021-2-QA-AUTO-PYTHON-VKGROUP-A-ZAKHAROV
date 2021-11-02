from urllib.parse import urlparse
from base import BaseCase
from ui.fixtures import *
from ui.locators.basic_locators import LoginPageLocators


class TestInvalidAuthorization(BaseCase):
    authorize = False

    @pytest.mark.UI
    def test_invalid_login(self, login_page):
        login_page.login(login='sasa60540', password='Azaza123', correct=False)
        assert login_page.find(LoginPageLocators.BAD_LOGIN_LOCATOR)

    @pytest.mark.UI
    def test_invalid_password(self, login_page):
        login_page.login(login='sasa60540@gmail.com', password='Azaza228', correct=False)
        assert urlparse(self.driver.current_url).netloc == 'account.my.com'


class TestCreateCompany(BaseCase):

    @pytest.mark.UI
    def test_create_company(self, create_campaign):
        assert create_campaign in self.driver.page_source


class TestSegment(BaseCase):

    @pytest.mark.UI
    def test_create_segment(self, create_segment):
        assert create_segment in self.driver.page_source

    @pytest.mark.UI
    def test_delete_segment(self,  delete_segment):
        assert delete_segment not in self.driver.page_source