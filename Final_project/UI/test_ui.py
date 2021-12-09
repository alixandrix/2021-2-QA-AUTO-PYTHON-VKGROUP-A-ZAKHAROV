from base import BaseCase
from faker import Faker
from selenium.common.exceptions import TimeoutException


class TestPositiveRegistration(BaseCase):

    def test_positive_registration(self, topic, client_mysql):
        username = topic.username
        reg_page = self.base_page.switch()
        main_p = reg_page.register(username, topic.password, topic.email)
        main_p.find(main_p.locators.LOGOUT_LOCATOR)
        assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
        user = client_mysql.get_data().filter_by(username=username).first().username
        client_mysql.delete_user(username)
        assert user

    def test_edge_registration(self, topic, client_mysql):
        fake = Faker()
        for i in range(3):
            print(i)
            username = fake.bothify('?'*15+i*'?')
            reg_page = self.base_page.switch()
            main_p = reg_page.register(username, topic.password, topic.email)
            try:
                main_p.find(main_p.locators.LOGOUT_LOCATOR)
            except TimeoutException:
                assert not client_mysql.get_data().filter_by(username=username).first()
            assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
            user = client_mysql.get_data().filter_by(username=username).first().username
            client_mysql.delete_user(username)
            assert user
        for i in range(3):
            password = (254 + i) * 'a'
            username = topic.username
            reg_page = self.base_page.switch()
            main_p = reg_page.register(username, password, topic.email)
            try:
                main_p.find(main_p.locators.LOGOUT_LOCATOR)
            except TimeoutException:
                assert not client_mysql.get_data().filter_by(username=username).first()
            assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
            user = client_mysql.get_data().filter_by(username=username).first().username
            client_mysql.delete_user(username)
            assert user
        for i in range(3):
            email = 54*'a'+'@'+'mail.'+'ru'+i*'u'
            username = topic.username
            reg_page = self.base_page.switch()
            main_p = reg_page.register(username, topic.password, email)
            try:
                main_p.find(main_p.locators.LOGOUT_LOCATOR)
            except TimeoutException:
                assert not client_mysql.get_data().filter_by(username=username).first()
            assert main_p.find((main_p.locators.LOGIN_LOCATOR[0], main_p.locators.LOGIN_LOCATOR[1].format(username)))
            user = client_mysql.get_data().filter_by(username=username).first().username
            client_mysql.delete_user(username)
            assert user


class TestNegativeRegistration(BaseCase):

    def test_negative_registration(self, topic, client_mysql):
       pass












