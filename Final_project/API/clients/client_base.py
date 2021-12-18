import logging
from urllib.parse import urljoin

import allure
import requests
from API.exceptions import *

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 666


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.term = 'y'
        self.submit_reg = 'Register'
        self.submit_login = 'Login'
        self.cookies = None
        self.session = requests.Session()

    @property
    def headers(self):
        return {
            'Cookie': self.cookies
        }

    @staticmethod
    def log_pre(url, headers, data, expected_status, json, files):
        logger.info(f'Performing request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'JSON: {json}\n\n'
                    f'FILES: {files}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  f'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n'
                            f'{response.text[:MAX_RESPONSE_LENGTH]}'
                            )
            elif logger.level == logging.DEBUG:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: {response.text}\n\n'
                            )
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n'
                        )

    @allure.step("Sending {method} request with headers:{headers}, data: {data}, json: {json} expected status = {expected_status}")
    def _request(self, method, url, headers=None, data=None, expected_status=200, jsonify=False, json=None, files=None):
        self.log_pre(url, headers, data, expected_status, json, files)
        response = self.session.request(method, url, headers=headers, data=data, json=json, files=files)
        self.log_post(response)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.request} for URL "{url}"')
        if jsonify:
            json_response = response.json()
            return json_response

        return response
