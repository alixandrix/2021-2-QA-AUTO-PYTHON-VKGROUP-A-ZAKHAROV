from ui.pages.main_page import MainPage
from ui.locators.basic_locators import LoginPageLocators, BasePageLocators
from ui.pages.base_page import BasePage
import logging
LOGIN = 'sasa60540@gmail.com'
PASSWORD = 'Azaza123'


class LoginPage(BasePage):
    locators = LoginPageLocators()


    def login(self, login=LOGIN, password=PASSWORD, correct=True):
        self.click(BasePageLocators.ENTER_LOCATOR)
        self.find(self.locators.LOGIN_LOCATOR).send_keys(login)
        self.find(self.locators.PASSW_LOCATOR).send_keys(password)
        self.click(self.locators.ENTER_LOCATOR)
        if correct:
            return MainPage(self.driver)



