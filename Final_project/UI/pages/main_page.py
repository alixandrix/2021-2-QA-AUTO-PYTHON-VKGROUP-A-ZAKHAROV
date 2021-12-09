import allure

from locators.basic_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):

    url = 'http://myapp:8060/welcome/'
    locators = MainPageLocators()

    @allure.step('Checking strange facts')
    def splash_buttons(self):
        pass

