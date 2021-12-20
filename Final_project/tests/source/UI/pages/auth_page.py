import allure
from selenium.common.exceptions import TimeoutException
from UI.pages.base_page import BasePage
from UI.pages.main_page import MainPage
from UI.locators.basic_locators import AuthPageLocators, MainPageLocators
from UI.utils.exceptions import ErrorAuthException

class AuthPage(BasePage):
    url = 'http://myapp_proxy:8070/reg'
    locators = AuthPageLocators()

    @allure.step('Registration with {login}, {password}, {email}')
    def register(self, login, password, email):
        self.find(self.locators.SUBMIT)
        self.find(self.locators.LOGIN_LOCATOR).send_keys(login)
        self.find(self.locators.EMAIL_LOCATOR).send_keys(email)
        self.find(self.locators.PASSW_LOCATOR).send_keys(password)
        self.find(self.locators.CONFIRM_PASSW_LOCATOR).send_keys(password)
        self.click(self.locators.SDET_LOCATOR)
        self.click(self.locators.SUBMIT)
        try:
            self.find(MainPageLocators.LOGOUT_LOCATOR)
            return MainPage(self.driver)
        except TimeoutException:
            print("/rError in registration!")
            return AuthPage(self.driver)

    @allure.step('Registration with {login}, {password}, {email} and without SDET')
    def register_SDET(self, login, password, email):
        self.find(self.locators.SUBMIT)
        self.find(self.locators.LOGIN_LOCATOR).send_keys(login)
        self.find(self.locators.EMAIL_LOCATOR).send_keys(email)
        self.find(self.locators.PASSW_LOCATOR).send_keys(password)
        self.find(self.locators.CONFIRM_PASSW_LOCATOR).send_keys(password)
        self.click(self.locators.SUBMIT)
        try:
            self.find(MainPageLocators.LOGOUT_LOCATOR)
            return MainPage(self.driver)
        except TimeoutException:
            print("/rError in registration!")
            raise ErrorAuthException





