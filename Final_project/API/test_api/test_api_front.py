import pytest
import allure
from API.exceptions import ResponseStatusCodeException
from API.test_api.base import ApiBase
from utils.creator import Builder


@allure.feature('API tests Front')
@pytest.mark.API
class TestApiAuth(ApiBase):
    authorize = False

    @pytest.mark.parametrize(
        'username, email, password',
        [
            (Builder.username(), Builder.email(), Builder.password()),
            (Builder.username(username_length=6), Builder.email(), Builder.password()),
            (Builder.username(), Builder.email(email_length=6), Builder.password()),
            (Builder.username(), Builder.email(), Builder.password(password_length=1)),
            (Builder.username(username_length=16), Builder.email(), Builder.password()),
            (Builder.username(), Builder.email(email_length=64), Builder.password()),
            (Builder.username(), Builder.email(), Builder.password(password_length=255))
        ]
    )
    def test_valid_auth(self, client_mysql, username, email, password):
        self.logger.info(f"Auth with {username}(length={len(username)}, {password} (length={len(password)}, {email} (length={len(email)}")
        self.api_client_front.post_auth(username, email, password)
        user = client_mysql.get_data(username=username).username
        assert user

    def test_invalid_auth_time(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.logger.info(f"Auth with {username}, {password}, {email}")
        self.api_client_front.post_auth(username, email, password)
        user = client_mysql.get_data(username=username).username
        time = client_mysql.get_data(username=username).start_active_time
        assert time is not None #bug
        assert user

    @pytest.mark.parametrize(
        'username, email, password',
        [
            (2*' ' + Builder.username(16), Builder.email(), Builder.password()),
            (Builder.username(), 2*' ' + Builder.email(email_length=63), Builder.password()),
            (Builder.username(), Builder.email(), 2*' ' + Builder.password(password_length=254)),
            (Builder.username(16) + 2 * ' ', Builder.email(), Builder.password()),
            (Builder.username(), Builder.email(email_length=63) + 2 * ' ', Builder.password()),
            (Builder.username(), Builder.email(), Builder.password(password_length=254) + 2 * '  ')
        ]
    )
    def test_invalid_auth_spaces(self, client_mysql, username, email, password):
        self.logger.info(f"Auth with {username}, {password}, {email}")
        self.api_client_front.post_auth(username, email, password)
        user = client_mysql.get_data(username=username).username
        assert user is None #password max 255, but 256 was given

    @pytest.mark.parametrize(
        'username, email, password',
        [
            (Builder.username(username_length=5), Builder.email(), Builder.password()),
            (Builder.username(), Builder.email(email_length=5), Builder.password()),
            (Builder.username(), Builder.email(), ''),
            (Builder.username(username_length=17), Builder.email(), Builder.password()),
            (Builder.username(), Builder.email(email_length=65), Builder.password()),
            (Builder.username(), Builder.email(), Builder.password(password_length=257))
        ]
    )
    def test_invalid_auth(self, client_mysql, username, email, password):
        with pytest.raises(ResponseStatusCodeException):
            self.logger.info(
                f"Auth with {username}(length={len(username)}, {password} (length={len(password)}, {email} (length={len(email)}")
            self.api_client_front.post_auth(username, email, password)
            user = client_mysql.get_data(username=username).username
            assert user is None # 500 not ok password

    def test_invalid_auth_and_logout(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.logger.info(f"Auth with {username}, {password}, {email} and then logout")
        self.api_client_front.post_auth(username, email, password)
        self.api_client_front.get_logout()
        user = client_mysql.get_data(username=username).username
        time = client_mysql.get_data(username=username).start_active_time
        assert time is not None # bug
        assert user

    def test_invalid_password_spaces(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = 'dsfd dsdsd'
        self.logger.info(f"Auth with {username}, {password}, {email}")
        self.api_client_front.post_auth(username, email, password)
        self.api_client_front.post_login(username, password)
        user = client_mysql.get_data(username=username).username
        assert user #пробелы внутри пароля не хорошо

@allure.feature('API tests Front')
@pytest.mark.API
class TestApiLogin(ApiBase):

    def test_valid_login(self, client_mysql):
        self.logger.info(f"Login with {self.user}, {self.password}")
        self.api_client_front.post_login(self.user, self.password)
        user = client_mysql.get_data(username=self.user).username
        active = client_mysql.get_data(username=self.user).active
        time = client_mysql.get_data(username=self.user).start_active_time
        assert time is not None
        assert active == 1
        assert user

    def test_invalid_login_email(self, client_mysql):
        self.logger.info(f"Login with {self.email}, {self.password}")
        self.api_client_front.post_login(self.email, self.password)
        active = client_mysql.get_data(username=self.user).active
        assert active == 0 #enter with space

    def test_invalid_login(self, client_mysql):
        username = self.builder.username()
        password = self.builder.password()
        self.logger.info(f"Invalid login with {username}, {password}")
        with pytest.raises(ResponseStatusCodeException):
            self.api_client_front.post_login(username, password)
            user = client_mysql.get_data(username=self.user).username
            assert user is None


@allure.feature('API tests Front')
@pytest.mark.API
class TestApiLogout(ApiBase):

    def test_invalid_login_and_logout(self, client_mysql):
        self.logger.info(f"Login with {self.user}, {self.password} and then logout")
        self.api_client_front.post_login(self.user, self.password)
        self.api_client_front.get_logout()
        user = client_mysql.get_data(username=self.user).username
        active = client_mysql.get_data(username=self.user).active
        time = client_mysql.get_data(username=self.user).start_active_time
        assert time is not None
        assert active == 0 # bug
        assert user






