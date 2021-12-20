import allure
import pytest

from API.test_api.base import ApiBase
from API.exceptions import ResponseStatusCodeException
from utils.creator import Builder

@allure.feature('API tests Back')
@pytest.mark.API
class TestApiAdd(ApiBase):

    @allure.description("Add user with doc api, expected status source = 201, but get 210")
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
    def test_valid_add_user(self, client_mysql, username, email, password):
        resp = self.api_client_back.post_add(username, email, password)
        user = client_mysql.get_data(username=username).username
        client_mysql.delete_user(username)
        assert resp.status_code == 201 #bug 201 expected
        assert user

    def test_valid_add_created(self, client_mysql):
        user = client_mysql.get_data(username=self.user).username
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.post_add(self.user, self.email, self.password)
            assert resp.status_code == 304
            assert user

    @allure.description("Add user with doc api, invalid data, but status source 201, and user add to db")
    @pytest.mark.parametrize(
        'username, email, password',
        [
            (Builder.username(username_length=5), Builder.email(), Builder.password()),
            (Builder.username(), Builder.email(email_length=5), Builder.password()),
            (Builder.username(), Builder.email(), '')
        ]
    )
    def test_invalid_add_user(self, client_mysql, username, email, password):
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.post_add(username, email, password)
            user = client_mysql.get_data(username=username)
            assert resp.status_code == 400 #201
            assert user is None #bug


@allure.feature('API tests Back')
@pytest.mark.API
class TestApiDel(ApiBase):

    def test_valid_del_user(self, client_mysql):
        resp = self.api_client_back.get_delete(self.user)
        user = client_mysql.get_data(username=self.user)
        assert resp.status_code == 204
        assert user is None

    def test_valid_del_user_twice(self, client_mysql):
        self.api_client_back.get_delete(self.user)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_delete(self.user)
            user = client_mysql.get_data(username=self.user).username
            assert resp.status_code == 404
            assert user is None

    def test_invalid_del_user(self, client_mysql):
        user = self.builder.username()
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_delete(user)
            user = client_mysql.get_data(username=self.user).username
            assert resp.status_code == 404
            assert user is None

    @allure.description("Add user with doc api then delete, status source = 204, but 200 expected")
    def test_valid_add_delete(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.api_client_back.post_add(username, email, password)
        resp = self.api_client_back.get_delete(username)
        user = client_mysql.get_data(username=username)
        assert resp.status_code == 200 #204
        assert user is None

    def test_valid_block_delete(self, client_mysql):
        self.api_client_back.get_block(self.user)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_delete(self.user)
            user = client_mysql.get_data(username=self.user)
            assert resp.status_code == 404
            assert user is None

@allure.feature('API tests Back')
@pytest.mark.API
class TestApiBlock(ApiBase):

    def test_valid_block(self, client_mysql):
        resp = self.api_client_back.get_block(self.user)
        access = client_mysql.get_data(username=self.user).access
        assert resp.status_code == 200
        assert access == 0

    def test_valid_block_twice(self, client_mysql):
        self.api_client_back.get_block(self.user)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_block(self.user)
            access = client_mysql.get_data(username=self.user).access
            assert resp.status_code == 304
            assert access == 0

    def test_invalid_block(self):
        username = self.builder.username()
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_block(username)
            assert resp.status_code == 404

    def test_valid_add_block(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.api_client_back.post_add(username, email, password)
        resp = self.api_client_back.get_block(username)
        user = client_mysql.get_data(username=username).username
        assert resp.status_code == 200
        assert user

    def test_invalid_delete_block(self, client_mysql):
        self.api_client_back.get_delete(self.user)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_block(self.user)
            user = client_mysql.get_data(username=self.user)
            assert resp.status_code == 404
            assert user is None

@allure.feature('API tests Back')
@pytest.mark.API
class TestApiUnblock(ApiBase):

    @allure.description("Block user then unblock with doc api, but status source 401, 304 expected")
    def test_valid_add_block_unblock(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.api_client_back.post_add(username, email, password)
        self.api_client_back.get_block(username)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_unblock(username)
            access = client_mysql.get_data(username=username).access
            assert resp.status_code == 200
            assert access == 1

    @allure.description("Block user then unblock with doc api, but status source 401, 304 expected")
    def test_valid_block_unblock(self, client_mysql):
        self.api_client_back.get_block(self.user)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_unblock(self.user)
            access = client_mysql.get_data(username=self.user).access
            assert resp.status_code == 200 #401
            assert access == 1

    def test_valid_unblock(self, client_mysql):
        resp = self.api_client_back.get_unblock(self.user)
        access = client_mysql.get_data(username=self.user).access
        assert resp.status_code == 304
        assert access == 1#

    def test_valid_unblock_twice(self, client_mysql):
        self.api_client_back.get_unblock(self.user)
        resp = self.api_client_back.get_unblock(self.user)
        access = client_mysql.get_data(username=self.user).access
        assert resp.status_code == 304
        assert access == 1#

    def test_invalid_unblock(self):
        username = self.builder.username()
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_unblock(username)
            assert resp.status_code == 404

    def test_valid_add_unblock(self, client_mysql):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.api_client_back.post_add(username, email, password)
        resp = self.api_client_back.get_unblock(username)
        user = client_mysql.get_data(username=username).username
        access = client_mysql.get_data(username=self.user).access
        assert resp.status_code == 304
        assert access == 1
        assert user

    def test_invalid_delete_unblock(self, client_mysql):
        self.api_client_back.get_delete(self.user)
        with pytest.raises(ResponseStatusCodeException):
            resp = self.api_client_back.get_unblock(self.user)
            user = client_mysql.get_data(username=self.user)
            assert resp.status_code == 404
            assert user is None

@allure.feature('API tests Back')
@pytest.mark.API
class TestApiStatus(ApiBase):

    def test_status(self):
        resp = self.api_client_back.get_status()
        assert resp.status_code == 200

    def test_add_status(self):
        username = self.builder.username()
        email = self.builder.email()
        password = self.builder.password()
        self.api_client_back.post_add(username, email, password)
        resp = self.api_client_back.get_status()
        assert resp.status_code == 200

    def test_delete_status(self):
        self.api_client_back.get_delete(self.user)
        resp = self.api_client_back.get_status()
        assert resp.status_code == 200

    def test_block_status(self):
        self.api_client_back.get_block(self.user)
        resp = self.api_client_back.get_status()
        assert resp.status_code == 200

    def test_unblock_status(self):
        self.api_client_back.get_unblock(self.user)
        resp = self.api_client_back.get_status()
        assert resp.status_code == 200












