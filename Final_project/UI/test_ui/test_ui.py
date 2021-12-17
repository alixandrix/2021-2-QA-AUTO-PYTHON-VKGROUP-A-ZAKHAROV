import random

import allure
import pytest

from base import BaseCase
from UI.locators import basic_locators
from utils.creator import Builder
from UI.utils.exceptions import ErrorLoginException, ErrorAuthException

@allure.feature('UI tests')
@pytest.mark.UI
class TestPositiveAuth(BaseCase):
    authorize = False


    def test_positive_auth(self, client_mysql):
        username = self.builder.username(username_length=10)
        password = self.builder.password(password_length=10)
        email = self.builder.email(email_length=10)
        self.logger.info(f"Auth with {username}, {password}, {email}")
        reg_page = self.base_page.switch()
        main_p = reg_page.register(username, password, email)
        main_p.find(main_p.locators.LOGOUT_LOCATOR)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
        user = client_mysql.get_data(username=username).username
        active = client_mysql.get_data(username=username).active
        time = client_mysql.get_data(username=username).start_active_time
        assert active != 1  # bug
        assert time is None  # bug
        assert user


    @pytest.mark.parametrize(
        'username',
        [
            Builder.username(username_length=6),
            Builder.username(username_length=15),
            Builder.username(username_length=16)
        ]
    )
    def test_positive_username_edge_auth(self, username, client_mysql):
        reg_page = self.base_page.switch()
        password = self.builder.password(password_length=11)
        email = self.builder.email(email_length=10)
        self.logger.info(f"Auth with {username} (length={len(username)}), {password}, {email}")
        main_p = reg_page.register(username, password, email)
        main_p.find(main_p.locators.LOGOUT_LOCATOR)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
        user = client_mysql.get_data(username=username).username
        assert user


    def test_positive_username_spaces(self, client_mysql):
        username = 7 * " " + self.builder.username(username_length=3)
        password = self.builder.password(password_length=8)
        email = self.builder.email(email_length=12)
        self.logger.info(f"Auth with {username} (but strip username{username.strip()}), {password}, {email}")
        reg_page = self.base_page.switch()
        main_p = reg_page.register(username, password, email)
        main_p.find(main_p.locators.LOGOUT_LOCATOR)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0],
                            main_p.locators.LOGIN_LOCATOR[1].format(username)))  # username without spaces
        user = client_mysql.get_data(username=username).username
        assert user


    @pytest.mark.parametrize(
        'password',
        [
            Builder.password(password_length=1),
            Builder.password(password_length=254),
            Builder.password(password_length=255),
        ]
    )
    def test_positive_password_edge_auth(self, password, client_mysql):
        username = self.builder.username(username_length=12)
        email = self.builder.email(email_length=12)
        self.logger.info(f"Auth with {username}, {password}(length={len(password)}), {email}")
        reg_page = self.base_page.switch()
        main_p = reg_page.register(username, password, email)
        main_p.find(main_p.locators.LOGOUT_LOCATOR)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
        user = client_mysql.get_data(username=username).username
        assert user


    @pytest.mark.parametrize(
        'email',
        [
            Builder.email(email_length=6),
            Builder.email(email_length=63),
            Builder.email(email_length=64)
        ]
    )
    def test_positive_email_edge_auth(self, email, client_mysql):
        password = self.builder.password(password_length=30)
        username = self.builder.username(username_length=12)
        self.logger.info(f"Auth with {username}, {password}, {email}(length={len(email)})")
        reg_page = self.base_page.switch()
        main_p = reg_page.register(username, password, email)
        main_p.find(main_p.locators.LOGOUT_LOCATOR)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
        user = client_mysql.get_data(username=username).username
        assert user

@allure.feature('UI tests')
@pytest.mark.UI
class TestTwoEmails(BaseCase):
    need_login = False

    def test_negative_two_emails(self, client_mysql):
        username = self.builder.username()
        password = self.builder.password()
        email = self.email
        self.logger.info(f"Auth with {username} , {password}, {email} which was registered yet")
        reg_page = self.base_page.switch()
        with pytest.raises(ErrorLoginException):
            reg_page.register(username, password, email)
            user = client_mysql.get_data(username=username).username
            assert user #500 response

@allure.feature('UI tests')
@pytest.mark.UI
class TestNegativeAuth(BaseCase):
    authorize = False


    def test_negative_one_empty_auth(self, client_mysql):
        auth_page = self.base_page.switch()
        for i in range(3):
            if i == 0:
                username = " "
                password = self.builder.password(password_length=20)
                email = self.builder.email(email_length=12)
            elif i == 1:
                email = ""
                password = self.builder.password(password_length=28)
                username = self.builder.username(username_length=14)
            else:
                username = self.builder.username(username_length=13)
                email = self.builder.email(email_length=10)
                password = ""
            auth_page.register(username, password, email)
            self.logger.info(f"Auth with {username}, {password}, {email}")
            assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
            assert client_mysql.get_data(username) is None


    def test_negative_one_full_auth(self, client_mysql):
        auth_page = self.base_page.switch()
        for i in range(3):
            if i == 0:
                username = " "
                password = ""
                email = self.builder.password(password_length=12)
            elif i == 1:
                email = ""
                password = self.builder.password(password_length=28)
                username = " "
            else:
                username = self.builder.username(username_length=13)
                email = ""
                password = ""
            auth_page.register(username, password, email)
            self.logger.info(f"Auth with {username}, {password}, {email}")
            assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
            assert client_mysql.get_data(username) is None

    @pytest.mark.parametrize(
        'username',
        [
            Builder.username(username_length=5),
            Builder.username(username_length=17)
        ]
    )
    def test_negative_username_edge_auth(self, username, client_mysql):
        password = self.builder.password(password_length=20)
        email = self.builder.email(email_length=12)
        self.logger.info(f"Auth with {username}(length={len(username)}, {password}, {email}")
        auth_page = self.base_page.switch()
        auth_page.register(username, password, email)
        assert auth_page.find(auth_page.locators.LOGIN_LOCATOR, timeout=15)
        assert client_mysql.get_data(username) is None

    def test_negative_password_edge_auth(self, client_mysql):
        username = self.builder.username(username_length=13)
        email = self.builder.email(email_length=14)
        password = self.builder.password(password_length=257)
        self.logger.info(f"Auth with {username}, {password}(length={len(password)}, {email}")
        auth_page = self.base_page.switch()
        auth_page.register(username, password, email)
        assert auth_page.find(auth_page.locators.LOGIN_LOCATOR,  timeout=15)
        assert client_mysql.get_data(username) is None

    @pytest.mark.parametrize(
        'email',
        [
            Builder.email(email_length=5),
            Builder.email(email_length=65)
        ]
    )
    def test_negative_email_edge_auth(self, email, client_mysql):
        username = self.builder.username(username_length=13)
        password = self.builder.password(password_length=50)
        self.logger.info(f"Auth with {username}, {password}, {email}(length={len(email)})")
        auth_page = self.base_page.switch()
        auth_page.register(username, password, email)
        assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
        assert client_mysql.get_data(username) is None

    def test_negative_SDET_auth(self, client_mysql):
        username = self.builder.username(username_length=13)
        password = self.builder.password(password_length=50)
        email = self.builder.email(email_length=14)
        auth_page = self.base_page.switch()
        with pytest.raises(ErrorAuthException):
            auth_page.register_SDET(username, password, email)
            assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
            assert client_mysql.get_data(username) is None

    def test_negative_nude(self, client_mysql):
        username = ' '
        password = ''
        email = ''
        self.logger.info(f"Auth with {username}, {password}, {email}")
        auth_page = self.base_page.switch()
        auth_page.register(username, password, email)
        assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
        assert client_mysql.get_data(username) is None #check

    def test_negative_spaces_password(self, client_mysql):
        username = self.builder.username(username_length=11)
        password = 3*" "+self.builder.password(password_length=5)
        email = self.builder.email(email_length=11)
        self.logger.info(f"Auth with {username}, spaces before password {password}, {email}")
        auth_page = self.base_page.switch()
        main_p = auth_page.register(username, password, email)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
        user = client_mysql.get_data(username=username).username
        password_db = client_mysql.get_data(username=username).password
        client_mysql.delete_user(username)
        assert password_db == password
        assert user #check

@allure.feature('UI tests')
@pytest.mark.UI
class TestMain(BaseCase):

    def test_positive_logout(self):
        self.logger.info(f"Check button logout")
        self.main_page.click(self.main_page.locators.LOGOUT_LOCATOR)
        assert self.main_page.find(self.base_page.locators.LOGIN_LOCATOR)

    def test_positive_vk(self):
        self.logger.info(f"Check VK_ID")
        self.main_page.driver.refresh()
        assert self.main_page.find(self.main_page.locators.VK_ID_LOCATOR) #check

    @pytest.mark.parametrize(
        'locator, expected_name',
        [
            (basic_locators.MainPageLocators.API_LOCATOR, 'API'),
            (basic_locators.MainPageLocators.INTERNET_FUTURE_LOCATOR, 'future'),
            (basic_locators.MainPageLocators.SMTP_LOCATOR, 'SMTP')
        ]
    )
    def test_positive_body(self, locator, expected_name):
        self.logger.info(f"Testing body content API")
        current_window = self.driver.current_window_handle
        self.main_page.click_new_window(locator)
        with self.switch_to_next_windows(current_window, close=True):
            assert expected_name in self.driver.current_url

    def test_positive_navbar_python(self):
        self.logger.info(f"Testing navbar clicking on Python")
        current_window = self.driver.current_window_handle
        self.main_page.click_new_window(self.main_page.locators.PYTHON_LOCATOR)
        with self.switch_to_next_windows(current_window, close=True):
            assert 'python' in self.driver.current_url        #check                  # другие элементы навбара не кликаются при развертывании списка

    @pytest.mark.parametrize(
        'locator_navbar, locator, expected_name',
        [
            (basic_locators.MainPageLocators.PYTHON_LOCATOR, basic_locators.MainPageLocators.PYTHON_HISTORY_LOCATOR,
             ['history']),
            (basic_locators.MainPageLocators.PYTHON_LOCATOR, basic_locators.MainPageLocators.FLASK_LOCATOR,
             ['flask']),
            (basic_locators.MainPageLocators.NETWORK_LOCATOR, basic_locators.MainPageLocators.WIRESHARK_NEWS_LOCATORS,
             ['news', 'wireshark']),
            (basic_locators.MainPageLocators.NETWORK_LOCATOR,
             basic_locators.MainPageLocators.WIRESHARK_DOWNLOAD_LOCATORS, ['download', 'wireshark']),
            (basic_locators.MainPageLocators.NETWORK_LOCATOR,
             basic_locators.MainPageLocators.TCPDUMP_LOCATOR, ['tcpdump-examples'])

        ]
    )
    def test_positive_navbar(self, locator_navbar, locator, expected_name):
        self.logger.info(f"Testing navbar")
        current_window = self.driver.current_window_handle
        self.main_page.click_navbar(locator_navbar,
                                    locator)
        with self.switch_to_next_windows(current_window, close=True):
            if len(expected_name) > 1:
                assert expected_name[0] in (self.driver.current_url).lower() and expected_name[1] in (self.driver.current_url).lower()
            else:
                assert expected_name[0] in (self.driver.current_url).lower() #check

    def test_negative_centos(self):
        self.logger.info(f"Testing navbar clicking on Centos, but Fedora is opening")
        current_window = self.driver.current_window_handle
        self.main_page.click_navbar(self.main_page.locators.LINUX_LOCATOR, self.main_page.locators.DOWNLOAD_CENTOS_LOCATOR)
        with self.switch_to_next_windows(current_window, close=True):
            assert 'centos' in self.driver.current_url and 'centos' in self.driver.page_source  # fedora != centos

@allure.feature('UI tests')
@pytest.mark.UI
class TestPositiveLoginPage(BaseCase):
    need_login = False

    def test_positive_login(self):
        self.logger.info(f"Testing normal login page")
        self.login_page.login(self.user, self.password)
        assert self.driver.current_url == 'http://myapp_proxy:8070/welcome/'

    def test_positive_login_spaces(self):
        self.logger.info(f"Testing normal login page")
        self.login_page.login((self.user+' '), self.password)
        assert self.driver.current_url == 'http://myapp_proxy:8070/welcome/'

    def test_positive_login_back_spaces(self):
        self.logger.info(f"Testing login page, while going back and add spaces")
        self.login_page.login(self.user, self.password)
        self.driver.back()
        self.login_page.find(self.login_page.locators.LOGIN_LOCATOR)
        main_p = self.login_page.login((self.user+10*' '), self.password)
        assert main_p.find(main_p.locators.INCORRECT_LENGTH_LOCATOR) #bug #check

    @pytest.mark.parametrize(
        'username, password',
        [
            ('', random.randint(1, 255)),
            (random.randint(6, 16), '')
        ]
    )
    def test_positive_fill_field(self, username, password):
        self.logger.info(f"Testing login page on not field fields")
        with pytest.raises(ErrorLoginException):
            self.login_page.login(username, password)
            assert self.driver.current_url == self.login_page.url and 'Please fill out this field' in self.driver.page_source

@allure.feature('UI tests')
@pytest.mark.UI
class TestNegativeLoginPage(BaseCase):
    need_login = False

    def test_negative_login(self):
        self.logger.info(f"Testing login page with not created username and password")
        with pytest.raises(ErrorLoginException):
            self.login_page.login(self.builder.username(), self.builder.password())
            assert self.driver.current_url == self.login_page.url and self.login_page.find(self.login_page.locators.ERROR_LOCATOR)

    def test_negative_login_email(self):
        self.logger.info(f"Testing login page with email not login")
        with pytest.raises(ErrorLoginException):
            self.login_page.login(self.email, self.password)
            assert self.driver.current_url == self.login_page.url and self.login_page.find(self.login_page.locators.ERROR_LOCATOR)

    def test_negative_without_login(self):
        self.logger.info(f"Testing login page without login")
        with pytest.raises(ErrorLoginException):
            self.login_page.login('', self.password)
            assert self.driver.current_url == self.login_page.url  and self.login_page.find(self.login_page.locators.ERROR_LOCATOR)

    def test_negative_password_spaces(self):
        self.logger.info(f"Testing login page without login")
        with pytest.raises(ErrorLoginException):
            self.login_page.login(self.user, (self.password+'  '))
            assert self.driver.current_url == self.login_page.url and self.login_page.find(self.login_page.locators.ERROR_LOCATOR)

    def test_negative_login_spaces(self):
        self.logger.info(f"Testing login page without login")
        with pytest.raises(ErrorLoginException):
            self.login_page.login(' ' + self.user, self.password)
            assert self.driver.current_url == self.login_page.url and self.login_page.find(self.login_page.locators.ERROR_LOCATOR)

@allure.feature('UI tests')
@pytest.mark.UI
class TestSpecial(BaseCase):

    def test_active(self, client_mysql):
        self.driver.close()
        active = client_mysql.get_data(username=self.user).active
        assert active == 0











