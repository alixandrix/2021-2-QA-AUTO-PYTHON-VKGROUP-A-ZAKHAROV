from selenium.webdriver.common.by import By

class BasePageLocators:
    ENTER_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')

class MainPageLocators:
    NAVBAR_AUDIENCE_LOCATOR = (By.XPATH, '//a[@href="/segments"]')
    NAVBAR_COMPANY_LOCATOR = (By.XPATH, '//a[@href="/dashboard"]')


class LoginPageLocators:
    LOGIN_LOCATOR = (By.NAME, 'email')
    PASSW_LOCATOR = (By.NAME, 'password')
    ENTER_LOCATOR = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
    BAD_LOGIN_LOCATOR = (By.XPATH, '//div[contains(@class, "notify-module-content")]')


class CompanyPageLocators:
    FIRST_CREATE_LOCATOR = (By.XPATH, '//a[@href="/campaign/new"]')
    HREF_LOCATOR = (By.XPATH, '//div[contains(@class, "nameCell-module-campaignNameCell")]//a[contains(@title, "{}")]')
    PRE_DELETE_LOCATOR = (By.XPATH,
                          '//div[contains(@data-test, "setting-{0} row-{0}")]//div[contains(@class, "icon-settings '
                          'settingsCell-module-settingsIcon")]')
    CREATE_LOCATOR = (By.XPATH, '//div[contains(@class, "button-module-blue")]')
    TRAFFIC_LOCATOR = (By.XPATH, '//div[contains(@class, "traffic")]')
    URL_LOCATOR = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    COMPANY_LOCATOR = (By.CSS_SELECTOR, "div[class='base-settings__campaign-name-wrap "
                                        "js-base-setting-campaign-name-wrap'] input[class='input__inp "
                                        "js-form-element']")
    BANNER_LOCATOR = (By.ID, 'patterns_banner_4')
    URL2_LOCATOR = (By.XPATH, '//input[contains(@class, "roles-module-roleSearchInput")]')
    UPLOAD_LOCATOR = (By.XPATH, '//input[contains(@data-test, "image_240x400")]')
    SAVE_PNG_LOCATOR = (By.XPATH, '//input[contains(@class, "image-cropper__save js-save")]')
    SAVE_COMPANY_LOCATOR = (By.CSS_SELECTOR, "div[class='footer__controls-wrap js-buttons-hidden-wrap'] button["
                                             "class='button button_submit']")
    CHECKER_LOCATOR = (By.XPATH, '//div[contains(@class, "notify-module-content")]/div[contains(@class, "icon-success '
                                 'toast-module-icon")]')
    DELETE_COMPANY_LOCATOR = (By.XPATH, '//ul[contains(@class, "optionsList-module-optionsList-")]//li[contains('
                                        '@class, "optionsList-module-option") and @data-id="3"]')


class SegmentsPageLocators:
    FIRST_CREATE_LOCATOR = (By.XPATH, '//a[@href="/segments/segments_list/new/"]')
    HREF_LOCATOR = (By.XPATH,
                    '//div[contains(@class, "cells-module-nameCell")]//a[contains(@title, "{}")]')
    PRE_DELETE_LOCATOR = (By.XPATH,
                          '//div[contains(@data-test, "remove-{0} row-{0}")]/span[contains(@class, "icon-cross '
                          'cells-module-removeCell")]')
    CREATE_LOCATOR = (By.XPATH, '//div[@class="segments-list__tbl-settings-wrap js-table-settings-wrap"]/div/button')
    TYPE_SEGMENT_LOCATOR = (By.XPATH, '//div[@class="adding-segments-modal__block-left js-sources-types"]//div[8]')
    CHECKBOX_LOCATOR = (By.XPATH, '//input[@class="adding-segments-source__checkbox js-main-source-checkbox"]')
    ADD_SEGMENT_LOCATOR = (By.XPATH, '//div[@class="adding-segments-modal__footer"]//button[@class="button '
                                     'button_submit"]')
    NAME_SEGMENT_LOCATOR = (By.XPATH, '//div[@class="input input_create-segment-form"]//input[@class="input__inp '
                                      'js-form-element"]')
    CREATE_SEGMENT_LOCATOR = (By.XPATH, '//div[@class="create-segment-form__btn-wrap '
                                        'js-create-segment-button-wrap"]/button[@class="button button_submit"]')
    CHECKER_LOCATOR = (By.XPATH, '//div[contains(@class, "main-module-Table")]')
    CONFIRM_REMOVE_LOCATOR = (By.XPATH, '//button[@class="button button_confirm-remove button_general"]')