from selenium.webdriver.common.by import By

ENTER1_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
LOGIN_LOCATOR = (By.NAME, 'email')
PASSW_LOCATOR = (By.NAME, 'password')
ENTER2_LOCATOR = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
BALANCE_LOCATOR = (By.XPATH, '//span[contains(@class, "js-head-balance")]')
INF_BUTT = (By.XPATH, '//div[contains(@class, "right-module-rightButton")]')
EXIT_LOCATOR = (By.XPATH, '//a[@href="/logout"]')