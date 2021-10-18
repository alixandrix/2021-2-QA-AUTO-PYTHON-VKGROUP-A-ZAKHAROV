from base import BaseCase
from ui.locators import basic_locators
import pytest
import time
FIO = 'Zakharov Alex Sergeevich'
TEL_NUMBER = '89001234567'


class TestOne(BaseCase):

    @pytest.mark.UI
    def test_login(self):
        self.login()
        assert self.find(basic_locators.BALANCE_LOCATOR)


    @pytest.mark.UI
    def test_logout(self):
        self.login()
        time.sleep(1)
        self.logout()
        assert self.find(basic_locators.ENTER1_LOCATOR)


    @pytest.mark.UI
    def test_fill_form(self):
        self.login()
        self.fill_form()
        assert self.find(basic_locators.FIO_LOCATOR).get_attribute('value') == FIO and self.find(basic_locators.TEL_NUMBER_LOCATOR).get_attribute('value') == TEL_NUMBER

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'locator, expected_url',
        [
                (basic_locators.PRO_LOCATOR, 'https://target.my.com/pro'),
            (basic_locators.COMPANY_LOCATOR, 'https://target.my.com/dashboard')

        ]
    )
    def test_run_site(self, locator, expected_url):
        self.login()
        time.sleep(1)
        self.find(locator).click()
        assert self.driver.current_url == expected_url



