from urllib.parse import urljoin

import allure
from client_front import ApiClientFront


class ApiClientBack(ApiClientFront):

    def __init__(self, base_url, cookies):
        super().__init__(base_url)
        self.cookies = cookies

    @property
    def header_cookie(self):
        return {'Cookie': f'session = {self.cookies}',
                'Host': self.base_url}

    @allure.step("Add user with {username}, {password}, {email}(back api)")
    def post_add(self, username, email, password):
        location = 'api/add_user'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session = {self.cookies}'
        }
        json = {
            "username": username,
            "password": password,
            "email": email
        }
        resp = self._request('POST', urljoin(self.base_url, location), headers=headers, json=json, expected_status=210)
        return resp

    @allure.step("Delete user {username} (back api)")
    def get_delete(self, username):
        location = f'api/del_user/{username}'
        resp = self._request('GET', urljoin(self.base_url, location), headers=self.header_cookie, expected_status=204)
        return resp

    @allure.step("Block user {username} (back api)")
    def get_block(self, username):
        location = f'api/block_user/{username}'
        resp = self._request('GET', urljoin(self.base_url, location), headers=self.header_cookie)
        return resp

    @allure.step("Unlock user {username} (back api)")
    def get_unblock(self, username):
        location = f'api/accept_user/{username}'
        resp = self._request('GET', urljoin(self.base_url, location), headers=self.header_cookie,  expected_status=304)
        print(resp.status_code)
        return resp

    @allure.step("Status of app(back api)")
    def get_status(self):
        location = 'status'
        resp = self._request('GET', urljoin(self.base_url, location))
        return resp


