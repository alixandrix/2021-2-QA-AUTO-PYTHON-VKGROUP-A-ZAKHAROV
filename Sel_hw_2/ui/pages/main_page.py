import allure
from ui.locators.basic_locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = MainPageLocators()

    @allure.step('Switch by locator {a}')
    def switcher(self, a):
        self.click(a)
        if a == self.locators.NAVBAR_AUDIENCE_LOCATOR:
            from ui.pages.segments_page import SegmentPage
            return SegmentPage(self.driver)
        elif a == self.locators.NAVBAR_COMPANY_LOCATOR:
            from ui.pages.company_page import CompanyPage
            return CompanyPage(self.driver)