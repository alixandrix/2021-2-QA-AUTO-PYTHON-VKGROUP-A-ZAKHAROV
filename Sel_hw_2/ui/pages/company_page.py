import allure
from selenium.common.exceptions import TimeoutException
from ui.locators.basic_locators import CompanyPageLocators
from ui.pages.created_company_page import CrCompanyPage
from ui.pages.main_page import MainPage
import ui.utils.creator as cr


class CompanyPage(MainPage):
    locators = CompanyPageLocators()

    @allure.step('Create company {name_company}')
    def create_company(self, my_dir, name_company):
        try:
            self.click(self.locators.CREATE_LOCATOR)
        except TimeoutException:
            self.click(self.locators.FIRST_CREATE_LOCATOR)
        self.click(self.locators.TRAFFIC_LOCATOR)
        with allure.step('Enter URL'):
            self.send_keys(self.locators.URL_LOCATOR, 'example.com')
        with allure.step('Enter name company'):
            self.send_keys(self.locators.COMPANY_LOCATOR, name_company)
        self.click(self.locators.BANNER_LOCATOR)
        with allure.step('Enter second URL'):
            self.send_keys(self.locators.URL2_LOCATOR, 'example.com')
        with allure.step('Upload picture'):
            input_field = self.find(self.locators.UPLOAD_LOCATOR)
            input_field.send_keys(cr.create_image(my_dir))
            self.click(self.locators.SAVE_PNG_LOCATOR)
        self.click(self.locators.SAVE_COMPANY_LOCATOR)


    @allure.step('Extract id from {name}')
    def extract_comp_id(self, name):
        href_locator = (self.locators.HREF_LOCATOR[0], self.locators.HREF_LOCATOR[1].format(name))
        href = self.find(href_locator).get_attribute('href')
        return str(''.join(i for i in href if i.isdigit()))

    @allure.step('Delete company with id={comp_id}')
    def delete_company(self, comp_id):
        deleter_locator = (self.locators.PRE_DELETE_LOCATOR[0], self.locators.PRE_DELETE_LOCATOR[1].format(comp_id))
        self.click(deleter_locator)
        self.click(self.locators.DELETE_COMPANY_LOCATOR)