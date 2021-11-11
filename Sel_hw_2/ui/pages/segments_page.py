import allure
from selenium.common.exceptions import TimeoutException
from ui.locators.basic_locators import SegmentsPageLocators
from ui.pages.main_page import MainPage


class SegmentPage(MainPage):
    locators = SegmentsPageLocators()
    url = 'https://target.my.com/segments/segments_list'

    @allure.step('Create segment {name}')
    def create_segments(self, name):
        try:
            self.click(self.locators.FIRST_CREATE_LOCATOR)
        except TimeoutException:
            self.click(self.locators.CREATE_LOCATOR)
            self.find(self.locators.TYPE_SEGMENT_LOCATOR)
        self.click(self.locators.CHECKBOX_LOCATOR)
        self.click(self.locators.ADD_SEGMENT_LOCATOR)
        with allure.step("Enter name segment"):
            self.send_keys(self.locators.NAME_SEGMENT_LOCATOR, name)

        self.click(self.locators.CREATE_SEGMENT_LOCATOR)
        self.find(self.locators.CHECKER_LOCATOR)

    @allure.step('Extract id from {name}')
    def extract_id(self, name):
        href_locator = (self.locators.HREF_LOCATOR[0], self.locators.HREF_LOCATOR[1].format(name))
        href = self.find(href_locator).get_attribute('href')
        return str(''.join(i for i in href if i.isdigit()))

    @allure.step('Delete segment with id={segm_id}')
    def delete_segment(self, segm_id):
        deleter_locator = (self.locators.PRE_DELETE_LOCATOR[0], self.locators.PRE_DELETE_LOCATOR[1].format(segm_id))
        self.click(deleter_locator)
        self.click(self.locators.CONFIRM_REMOVE_LOCATOR)