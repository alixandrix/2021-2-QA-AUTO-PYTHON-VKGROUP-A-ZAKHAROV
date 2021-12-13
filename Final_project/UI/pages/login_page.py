import allure
from selenium.common.exceptions import TimeoutException
from locators.basic_locators import LoginPageLocators, MainPageLocators
from pages.base_page import BasePage
from pages.main_page import MainPage


class LoginPage(BasePage):

    url = 'http://myapp:8060/'
    locators = LoginPageLocators()

    @allure.step('login with {username} {password}')
    def login(self, username, password):
        login_input = self.find(self.locators.LOGIN_LOCATOR)
        login_input.send_keys(username)
        self.find(self.locators.PASSWORD_LOCATOR).send_keys(password)
        self.click(self.locators.CONFIRM_LOCATOR)
        try:
            self.find(MainPageLocators.LOGOUT_LOCATOR)
        except TimeoutException:
            print("/rError in registration!")
        return MainPage(self.driver)
