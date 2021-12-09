from selenium.webdriver.common.by import By


class BasePageLocators:
    CREATE_ACCOUNT = (By.XPATH, '//a[@href="/reg"]')
    LOGIN_LOCATOR = (By.ID, "username")
    PASSWORD_LOCATOR = (By.ID, "password")
    CONFIRM_LOCATOR = (By.ID, "submit")


class MainPageLocators:
    LOGIN_LOCATOR = (By.XPATH, '//div[@id="login-name"]//li[text()="Logged as {}"]')
    API_LOCATOR = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]/img['
                             '@src="/static/images/laptop.png"]')
    INTERNET_FUTURE_LOCATOR = (By.XPATH, '//a[@href="https://www.popularmechanics.com/technology/infrastructure'
                                         '/a29666802/future-of-the-internet/"]/img[ '
                                         '@src="/static/images/loupe.png"]')
    SMTP_LOCATOR = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]/img[@src="/static/images/analytics.png"]')
    HOME_LOCATOR = (By.XPATH, '//li/a[@href="/"]')
    TM_VERSION_LOCATOR = (By.XPATH, '//ul/a[@class="uk-navbar-brand uk-hidden-small"]')
    PYTHON_LOCATOR = (By.XPATH, '//li/a[@href="https://www.python.org/"]')
    PYTHON_HISTORY_LOCATOR = (By.XPATH, '//li/a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    FLASK_LOCATOR = (By.XPATH, '//li/a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    LINUX_LOCATOR = (By.XPATH, '//li/a[@href="javascript:" and contains(text(), "Linux")]')
    DOWNLOAD_CENTOS_LOCATOR = (By.XPATH, '//li/a[@href="https://getfedora.org/ru/workstation/download/"]')
    NETWORK_LOCATOR = (By.XPATH, '//li/a[@href="javascript:" and contains(text(), "Network")]')
    WIRESHARK_NEWS_LOCATORS = (By.XPATH, '//li/a[@href="https://www.wireshark.org/news/"]')
    WIRESHARK_DOWNLOAD_LOCATORS = (By.XPATH, '//li/a[@href="https://www.wireshark.org/#download"]')
    TCPDUMP_LOCATOR = (By.XPATH, '//li/a[@href="https://hackertarget.com/tcpdump-examples/"]')
    LOGOUT_LOCATOR = (By.XPATH, '//div/a[@href="/logout"]')


class RegistrPageLocators:
    SUBMIT = (By.ID, "submit")
    LOGIN_LOCATOR = (By.ID, "username")
    EMAIL_LOCATOR = (By.ID, "email")
    PASSW_LOCATOR = (By.ID, "password")
    CONFIRM_PASSW_LOCATOR = (By.ID, "confirm")
    SDET_LOCATOR = (By.ID, "term")
    FLASH_LOCATOR = (By.ID, "flash")
