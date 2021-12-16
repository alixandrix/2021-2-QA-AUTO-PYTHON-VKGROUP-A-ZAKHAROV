from urllib.parse import urljoin
from API.clients.client_base import ApiClient

class ApiClientFront(ApiClient):

    def post_registration(self, user, email, password):
        location = 'reg'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        data = {
            'username': user,
            'email': email,
            'password': password,
            'confirm': password,
            'term': self.term,
            'submit': self.submit
        }
        self._request('POST', urljoin(self.base_url, location), headers=headers, data=data)
        self.cookies = self.session.cookies.get('session')
        #self._request('GET', urljoin(self.base_url, location_welc))