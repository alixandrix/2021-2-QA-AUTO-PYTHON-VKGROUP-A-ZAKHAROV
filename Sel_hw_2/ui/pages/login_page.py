import allure
from ui.locators.basic_locators import LoginPageLocators, BasePageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @allure.step('Login with {login}, {password}')
    def login(self, login, password, correct=True):
        self.click(BasePageLocators.ENTER_LOCATOR)
        self.find(self.locators.LOGIN_LOCATOR).send_keys(login)
        self.find(self.locators.PASSW_LOCATOR).send_keys(password)
        self.click(self.locators.ENTER_LOCATOR)
        if correct:
            return MainPage(self.driver)