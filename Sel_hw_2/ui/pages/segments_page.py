import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import ui.utils.creator as cr
from ui.locators.basic_locators import SegmentsPageLocators
from ui.pages.main_page import MainPage


class SegmentPage(MainPage):
    locators = SegmentsPageLocators()
    url = 'https://target.my.com/segments/segments_list'

    @allure.step('Create segment {name}')
    def create_segments(self, name):
        try:
            self.click(self.locators.CREATE_LOCATOR)
            self.find(self.locators.TYPE_SEGMENT_LOCATOR)
        except TimeoutException:
            self.click(self.locators.FIRST_CREATE_LOCATOR)
        self.click(self.locators.CHECKBOX_LOCATOR)
        self.click(self.locators.ADD_SEGMENT_LOCATOR)
        with allure.step("Enter name segment"):
            my_name = self.find(self.locators.NAME_SEGMENT_LOCATOR)
            my_name.clear()
            my_name.send_keys(name)
        self.click(self.locators.CREATE_SEGMENT_LOCATOR)
        self.find(self.locators.CHECKER_LOCATOR)

    @allure.step('Extract id from {name}')
    def extract_id(self, name):
        HREF_LOCATOR = (By.XPATH,
                        f'//div[contains(@class, "cells-module-nameCell")]//a[contains(@title, "{name}")]')
        href = self.find(HREF_LOCATOR).get_attribute('href')
        id_segment = str(''.join(i for i in href if i.isdigit()))
        return id_segment

    @allure.step('Delete segment with id={segm_id}')
    def delete_company(self, segm_id):
        PRE_DELETE_LOCATOR = (By.XPATH,
                              f'//div[contains(@data-test, "remove-{segm_id} row-{segm_id}")]/span[contains(@class, "icon-cross cells-module-removeCell")]')
        self.click(PRE_DELETE_LOCATOR)
        self.click(self.locators.CONFIRM_REMOVE_LOCATOR)





