import logging
from urllib.parse import urljoin
from utils.creator import create_image as cr
import requests
from api.exceptions import *
from api.data import *

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 666


class ApiClient:

    def __init__(self, base_url, login_url, user, password):
        self.base_url = base_url
        self.login_url = login_url
        self.user = user
        self.password = password
        self.session = requests.Session()

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
                  'RESPONSE STATUS: {response.status_code}'

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

    def post_login(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': self.base_url,
        }
        data = {
            'email': self.user,
            'password': self.password,
            'continue': urljoin(self.base_url, 'auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email'),
            'failure': urljoin(self.base_url, 'login/')
        }
        self._request('POST', self.login_url, headers=headers, data=data)
        self._request('GET', urljoin(self.base_url, 'scss/'), expected_status=404)

    def post_segment_create(self, name_segment):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': self.session.cookies.get('csrftoken'),
        }
        json = post_segment_create_json(name_segment)
        res = self._request('POST', urljoin(self.base_url, 'api/v2/remarketing/segments.json?fields=relations__object_type,'
                            'relations__object_id,relations__params,relations__id,id,name,pass_condition'),
                            headers=headers, json=json, jsonify=True)
        return res['id']

    def get_segment_id(self, name_segment):
        resp = self._request('GET', urljoin(self.base_url, 'api/v2/remarketing/segments.json'), jsonify=True)
        for i in resp['items']:
            if i['name'] == name_segment:
                return i['id']

    def delete_segment_id(self, id_segment):
        headers = {
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }
        return self._request('DELETE', urljoin(self.base_url, f'api/v2/remarketing/segments/{id_segment}.json'),
                             headers=headers, expected_status=204)

    def get_id_url(self):
        resp = self._request('GET', urljoin(self.base_url, 'api/v1/urls/?url=http%3A%2F%2Fexample.com%2F'),
                             jsonify=True)
        return resp['id']

    def post_image_id(self, my_dir):
        headers1 = {
            'Referer': urljoin(self.base_url, 'campaign/new'),
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }
        image_file = {
            'file': open(cr(my_dir), 'rb')
        }
        res1 = self._request('POST', urljoin(self.base_url, 'api/v2/content/static.json'), headers=headers1,
                             files=image_file,
                             jsonify=True)
        headers2 = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Referer': urljoin(self.base_url, 'campaign/new'),
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }
        json = {
            "description": "Image.png",
            "content": {
                "id": res1['id']
            }
        }
        self._request('POST', urljoin(self.base_url, 'api/v2/mediateka.json'), headers=headers2, json=json,
                      expected_status=201)
        return res1['id']

    def post_create_campaign(self, name_campaign, my_dir):
        headers = {
            'Content-Type': 'application/json',
            'referer': urljoin(self.base_url, 'campaign/new'),
            'X-Campaign-Create-Action': 'new',
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }
        json = post_create_campaign_json(name_campaign, self.get_id_url(), self.post_image_id(my_dir))
        res = self._request('POST', urljoin(self.base_url, 'api/v2/campaigns.json'), headers=headers, json=json,
                            jsonify=True)
        return res['id']

    def get_campaign_id(self, comp_id):
        return self._request('GET', urljoin(self.base_url, f'api/v2/campaigns.json?_id={comp_id}'), jsonify=True)['items'][0]['id']

    def post_delete_campaign(self, comp_id):
        headers = {
            'Content-Type': 'application/json',
            'referer': urljoin(self.base_url, 'dashboard'),
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }
        json = {'status': "deleted"}
        self._request('POST', urljoin(self.base_url, f'api/v2/campaigns/{comp_id}.json'), headers=headers, json=json,
                      expected_status=204)
