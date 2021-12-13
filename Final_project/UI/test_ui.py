import pytest

from base import BaseCase
from utils.creator import Builder


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
        client_mysql.delete_user(username)
        assert active == 0  # bug
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
        client_mysql.delete_user(username)
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
        client_mysql.delete_user(username)
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
        client_mysql.delete_user(username)
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
        client_mysql.delete_user(username)
        assert user



class TestNegativeAuth(BaseCase):
    authorize = False

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

    def test_positive_vk(self, fast_registration):
        self.logger.info(f"Check VK_ID")
        main_p = fast_registration
        main_p.driver.refresh()
        assert main_p.find(main_p.locators.VK_ID_LOCATOR)

    def test_positive_body(self, fast_registration):
        self.logger.info(f"Testing body content")





