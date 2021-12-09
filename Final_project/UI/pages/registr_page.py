import allure
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from pages.main_page import MainPage
from locators.basic_locators import RegistrPageLocators


class RegistrationPage(BasePage):
    url = 'http://myapp:8060/reg'
    locators = RegistrPageLocators()

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
            self.find(self.locators.FLASH_LOCATOR)
            print("Error in registration!")
        except TimeoutException:
            return MainPage(self.driver)





