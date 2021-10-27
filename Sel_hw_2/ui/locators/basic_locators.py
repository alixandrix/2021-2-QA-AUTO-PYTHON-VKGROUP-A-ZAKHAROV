from selenium.webdriver.common.by import By


class BasePageLocators:
    ENTER_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')

class LoginPageLocators:
    LOGIN_LOCATOR = (By.NAME, 'email')
    PASSW_LOCATOR = (By.NAME, 'password')
    ENTER_LOCATOR = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
    BAD_LOGIN_LOCATOR = (By.XPATH, '//div[contains(@class, "notify-module-content")]')

class CompanyPageLocators:
    CREATE_LOCATOR = (By.XPATH, '//div[contains(@class, "button-module-textWrapper")]')
    TRAFFIC_LOCATOR = (By.XPATH, '//div[contains(@class, "traffic")]')
    URL_LOCATOR = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    COMPANY_LOCATOR = (By.CSS_SELECTOR, "div[class='base-settings__campaign-name-wrap js-base-setting-campaign-name-wrap'] input[class='input__inp js-form-element']")
    BANNER_LOCATOR = (By.ID, 'patterns_banner_4')
    URL2_LOCATOR = (By.XPATH, '//input[contains(@class, "roles-module-roleSearchInput")]')
    UPLOAD_LOCATOR = (By.XPATH, '//input[contains(@data-test, "image_240x400")]')
    SAVE_PNG_LOCATOR = (By.XPATH, '//input[contains(@class, "image-cropper__save js-save")]')
    SAVE_COMPANY_LOCATOR = (By.CSS_SELECTOR, "div[class='footer__controls-wrap js-buttons-hidden-wrap'] button[class='button button_submit']")


