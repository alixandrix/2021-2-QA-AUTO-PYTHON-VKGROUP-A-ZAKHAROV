import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
#from ui.fixtures import *
from ui.locators.basic_locators import CompanyPageLocators
from ui.pages.created_company_page import CrCompanyPage
from ui.pages.main_page import MainPage
import ui.utils.creator as cr


class CompanyPage(MainPage):
    locators = CompanyPageLocators()

    @allure.step('Create company {name_company}')
    def create_company(self, my_dir, name_company):
        try:
            self.click(self.locators.FIRST_CREATE_LOCATOR)
        except TimeoutException:
            self.click(self.locators.CREATE_LOCATOR)
        self.click(self.locators.TRAFFIC_LOCATOR)
        with allure.step('Enter URL'):
            my_url = self.find(self.locators.URL_LOCATOR)
            my_url.clear()
            my_url.send_keys('example.com')
        my_name = self.find(self.locators.COMPANY_LOCATOR)
        my_name.clear()
        my_name.send_keys(name_company)
        self.click(self.locators.BANNER_LOCATOR)
        my_url = self.find(self.locators.URL2_LOCATOR)
        my_url.clear()
        my_url.send_keys('example.com')
        ##################################
        input_field = self.find(self.locators.UPLOAD_LOCATOR)
        input_field.send_keys(cr.create_image(my_dir))
        self.click(self.locators.SAVE_PNG_LOCATOR)
        self.click(self.locators.SAVE_COMPANY_LOCATOR)
        return CrCompanyPage(self.driver)

    @allure.step('Extract id from {name}')
    def extract_id(self, name):
        HREF_LOCATOR = (By.XPATH,
                        f'//div[contains(@class, "nameCell-module-campaignNameCell")]//a[contains(@title, "{name}")]')
        href = self.find(HREF_LOCATOR).get_attribute('href')
        id_company = str(''.join(i for i in href if i.isdigit()))
        return id_company

    @allure.step('Delete company with id={comp_id}')
    def delete_company(self, comp_id):
        PRE_DELETE_LOCATOR = (By.XPATH,
                              f'//div[contains(@data-test, "setting-{comp_id} row-{comp_id}")]//div[contains(@class, "icon-settings settingsCell-module-settingsIcon")]')
        self.click(PRE_DELETE_LOCATOR)
        self.click(self.locators.DELETE_COMPANY_LOCATOR)








