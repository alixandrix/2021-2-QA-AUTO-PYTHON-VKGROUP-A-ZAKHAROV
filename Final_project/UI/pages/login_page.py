import allure
from selenium.common.exceptions import TimeoutException
from UI.locators.basic_locators import LoginPageLocators, MainPageLocators
from UI.pages.base_page import BasePage
from UI.pages.main_page import MainPage
from UI.utils.exceptions import ErrorLoginException

class LoginPage(BasePage):

    url = 'http://myapp_proxy:8070/'
    locators = LoginPageLocators()

    @allure.step('login with {username} {password}')
    def login(self, username, password):
        self.find(self.locators.LOGIN_LOCATOR).send_keys(username)
        self.find(self.locators.PASSWORD_LOCATOR).send_keys(password)
        self.click(self.locators.CONFIRM_LOCATOR)
        try:
            self.find(MainPageLocators.LOGOUT_LOCATOR)
        except TimeoutException:
            raise ErrorLoginException
        return MainPage(self.driver)
