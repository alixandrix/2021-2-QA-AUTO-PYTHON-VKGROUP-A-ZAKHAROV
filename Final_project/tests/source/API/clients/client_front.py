from urllib.parse import urljoin
from API.clients.client_base import ApiClient
import allure


class ApiClientFront(ApiClient):

    @property
    def post_headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': self.base_url[7:-1]
        }

    @allure.step("Auth with {user}, {password}, {email}(front api)")
    def post_auth(self, user, email, password):
        location = 'reg'
        data = {
            'username': user,
            'email': email,
            'password': password,
            'confirm': password,
            'term': self.term,
            'submit': self.submit_reg
        }
        self._request('POST', urljoin(self.base_url, location), headers=self.post_headers, data=data)
        self.cookies = self.session.cookies.get('session')
        return self.cookies


    @allure.step("Login with {user}, {password}(front api)")
    def post_login(self, user, password):
        location = 'login'
        data = {
            'username': user,
            'password': password,
            'submit': self.submit_login
        }

        resp = self._request('POST', urljoin(self.base_url, location), headers=self.post_headers, data=data)
        return resp


    @allure.step(f"Logout(front api)")
    def get_logout(self):
        location = 'logout'
        self._request('GET', urljoin(self.base_url, location), headers=self.headers)



