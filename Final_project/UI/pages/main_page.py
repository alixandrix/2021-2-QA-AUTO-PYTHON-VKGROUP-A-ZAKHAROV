import allure

from UI.locators.basic_locators import MainPageLocators
from UI.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class MainPage(BasePage):

    url = 'http://myapp_proxy:8070/welcome/'
    locators = MainPageLocators()

    @allure.step('Clicking and open in new window')
    def click_new_window(self, locator):
        self.action_chains.key_down(Keys.COMMAND).click(locator).key_up(Keys.COMMAND).perform()

    @allure.step('Clicking on elements in navbar')
    def click_navbar(self, locator_nav, locator):
        button = self.find(locator_nav)
        self.action_chains.move_to_element(button).perform()
        self.click_new_window(locator)



