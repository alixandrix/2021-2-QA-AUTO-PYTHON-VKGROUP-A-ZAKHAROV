from urllib.parse import urljoin
from API.clients.client_base import ApiClient

class ApiClientFront(ApiClient):

    @property
    def post_headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

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


    def post_login(self, user, password):
        location = 'login'
        data = {
            'username': user,
            'password': password,
            'submit': self.submit_login
        }
        self._request('POST', urljoin(self.base_url, location), headers=self.post_headers, data=data)

    def get_logout(self):
        headers = {
            'Cookie': self.cookies
        }
        location = 'logout'
        self._request('GET', urljoin(self.base_url, location), headers=headers)



