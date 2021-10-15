from selenium.webdriver.common.by import By
FIO = 'Zakharov Alex Sergeevich'

ENTER1_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
LOGIN_LOCATOR = (By.NAME, 'email')
PASSW_LOCATOR = (By.NAME, 'password')
ENTER2_LOCATOR = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
BALANCE_LOCATOR = (By.XPATH, '//span[contains(@class, "js-head-balance")]')
INF_BUTT = (By.XPATH, '//div[contains(@class, "right-module-rightButton")]')
EXIT_LOCATOR = (By.XPATH, '//a[@href="/logout"]')
PROFILE_LOCATOR = (By.XPATH, '//a[@href="/profile"]')
FIO_LOCATOR = (By.CSS_SELECTOR, "div[class='js-contacts-field-name profile__list__row__input'] input[class='input__inp js-form-element']")
TEL_NUMBER_LOCATOR = (By.CSS_SELECTOR, "div[class='js-contacts-field-phone profile__list__row__input'] input[class='input__inp js-form-element']")
BUTTON_SAVE_LOCATOR = (By.XPATH, '//button[contains(@class, "button button_submit")]')
MAIN_LOGO_LOCATOR = (By.XPATH, '//a[@href="//target.my.com"]')
CHECK_FIO_LOCATOR = (By.XPATH, '//div[contains(@class, "right-module-userNameWrap")]')