import time

from ui.pages.main_page import MainPage
from ui.locators.basic_locators import CompanyPageLocators
from ui.pages.base_page import BasePage
import ui.utils.creator as cr
from ui.fixtures import *
LOGIN = 'sasa60540@gmail.com'
PASSWORD = 'Azaza123'


class CompanyPage(BasePage):
    locators = CompanyPageLocators()
    name_company = cr.create_name()
    url = 'https://target.my.com/dashboard'

    def create_company(self, my_dir):
        self.click(self.locators.CREATE_LOCATOR)
        self.click(self.locators.TRAFFIC_LOCATOR)
        my_url = self.find(self.locators.URL_LOCATOR)
        my_url.clear()
        my_url.send_keys('example.com')
        my_name = self.find(self.locators.COMPANY_LOCATOR)
        my_name.clear()
        my_name.send_keys(self.name_company)
        self.click(self.locators.BANNER_LOCATOR)
        my_url = self.find(self.locators.URL2_LOCATOR)
        my_url.clear()
        my_url.send_keys('example.com')
        ##################################
        input_field = self.find(self.locators.UPLOAD_LOCATOR)
        input_field.send_keys(cr.create_image(my_dir))
        self.click(self.locators.SAVE_PNG_LOCATOR)
        self.click(self.locators.SAVE_COMPANY_LOCATOR)
        time.sleep(5)





