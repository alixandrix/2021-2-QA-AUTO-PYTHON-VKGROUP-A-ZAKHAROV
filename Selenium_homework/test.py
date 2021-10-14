from base import BaseCase
from ui.locators import basic_locators
import pytest
import time

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
