import allure
import pytest

from base import BaseCase
from locators import basic_locators
from utils.creator import Builder
from fixtures import main_page

class TestPositiveAuth(BaseCase):
    authorize = False

    @allure.feature('UI tests')
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
        client_mysql.delete_user(username)
        assert active == 0  # bug
        assert time is None  # bug
        assert user

    @allure.feature('UI tests')
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
        client_mysql.delete_user(username)
        assert user

    @allure.feature('UI tests')
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
        client_mysql.delete_user(username)
        assert user

    @allure.feature('UI tests')
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
        client_mysql.delete_user(username)
        assert user

    @allure.feature('UI tests')
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
        client_mysql.delete_user(username)
        assert user


class TestNegativeAuth(BaseCase):
    authorize = False

    @allure.feature('UI tests')
    def test_negative_one_empty_auth(self, client_mysql):
        auth_page = self.base_page.switch()
        for i in range(3):
            if i == 0:
                username = " "
                password = self.builder.password(password_length=20)
                email = self.builder.password(email_length=12)
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

    @allure.feature('UI tests')
    def test_negative_one_full_auth(self, client_mysql):
        auth_page = self.base_page.switch()
        for i in range(3):
            if i == 0:
                username = " "
                password = ""
                email = self.builder.password(email_length=12)
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
        assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
        assert client_mysql.get_data(username) is None

    def test_negative_password_edge_auth(self, client_mysql):
        username = self.builder.username(username_length=13)
        email = self.builder.email(email_length=14)
        password = self.builder.password(password_length=257)
        self.logger.info(f"Auth with {username}, {password}(length={len(password)}, {email}")
        auth_page = self.base_page.switch()
        auth_page.register(username, password, email)
        assert auth_page.find(auth_page.locators.LOGIN_LOCATOR)
        assert client_mysql.get_data(username) is None

    @pytest.mark.parametrize(
        'email',
        [
            Builder.email(email_length=5),
            Builder.email(email_length=64)
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
        assert client_mysql.get_data(username) is None

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
        assert user

class TestPositiveMain(BaseCase):

    def test_positive_logout(self):
        self.logger.info(f"Check button logout")
        self.main_page.click(self.main_page.locators.LOGOUT_LOCATOR)
        assert self.main_page.find(self.base_page.locators.LOGIN_LOCATOR)

    def test_positive_vk(self):
        self.logger.info(f"Check VK_ID")
        self.main_page.driver.refresh()
        assert self.main_page.find(self.main_page.locators.VK_ID_LOCATOR)

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
            assert 'python' in self.driver.current_url                          # другие элементы навбара не кликаются при развертывании списка

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
        self.logger.info(f"Testing navbar clicking on Centos, but Fedora is opening")
        current_window = self.driver.current_window_handle
        self.main_page.click_navbar(locator_navbar,
                                    locator)
        with self.switch_to_next_windows(current_window, close=True):
            if len(expected_name) > 1:
                assert expected_name[0] in (self.driver.current_url).lower() and expected_name[1] in (self.driver.current_url).lower()
            else:
                assert expected_name[0] in (self.driver.current_url).lower()

    def test_positive_centos(self):
        self.logger.info(f"Testing navbar clicking on Centos, but Fedora is opening")
        current_window = self.driver.current_window_handle
        self.main_page.click_navbar(self.main_page.locators.LINUX_LOCATOR, self.main_page.locators.DOWNLOAD_CENTOS_LOCATOR)
        with self.switch_to_next_windows(current_window, close=True):
            assert 'fedora' in self.driver.current_url    # fedora != centos


class TestPositiveLoginPage(BaseCase):
    authorize = False
    #впихнуть еще 1 флаг на логин в бэйс

    def test_positive_login(self):
        self.logger.info(f"Testing login page")
        self.login_page.login(self.user, self.password)
        assert self.driver.current_url == self.main_page.url





#login_page: make test email:password



