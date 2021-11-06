import logging
from urllib.parse import urljoin
from utils.creator import create_image as cr
import requests

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 666


class InvalidLoginException(Exception):
    pass


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


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
            if json_response.get('bStateError'):
                error = json_response.get('sErrorMsg', 'Unknown')
                raise ResponseErrorException(f'Request "{url}" returned error "{error}"')
            return json_response

        return response

    def post_login(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': 'https://target.my.com/',
        }
        data = {
            'email': self.user,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self._request('POST', self.login_url, headers=headers, data=data)
        self._request('GET', urljoin(self.base_url, 'scss/'), expected_status=404)

    def post_segment_create(self, name_segment):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'referer': 'https://target.my.com/',
            'X-CSRFToken': self.session.cookies.get('csrftoken'),
        }
        json = {"name": name_segment,
                "pass_condition": 1,
                "relations": [{"object_type": "remarketing_player",
                               "params": {"type": "positive",
                                          "left": 365,
                                          "right": 0}}],
                "logicType": "or"}
        res = self._request('POST',
                            'https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,'
                            'relations__object_id,relations__params,relations__params__score,relations__id,'
                            'relations_count, '
                            'id,name,pass_condition,created,campaign_ids,users,flags',
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
            'Referer': 'https://target.my.com/campaign/new',
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
            'Referer': 'https://target.my.com/campaign/new',
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

    def post_create_campaign(self, name_campaign, my_dir, null=None, false=False, true=True):
        url_id = self.get_id_url()
        image_id = self.post_image_id(my_dir)
        headers = {
            'Content-Type': 'application/json',
            'referer': 'https://target.my.com/campaign/new',
            'X-Campaign-Create-Action': 'new',
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }

        json = {
            "name": name_campaign,
            "read_only": false,
            "conversion_funnel_id": null,
            "objective": "traffic",
            "enable_offline_goals": false,
            "targetings": {
                "split_audience": [
                    1,
                    2,
                ],
                "sex": [
                    "male",
                    "female"
                ],
                "age": {
                    "age_list": [
                        0,
                        12,
                        13,
                        14,
                        15

                    ],
                    "expand": true
                },
                "geo": {
                    "regions": [
                        188
                    ]
                },
                "interests_soc_dem": [],
                "segments": [],
                "interests": [],
                "fulltime": {
                    "flags": [
                        "use_holidays_moving",
                        "cross_timezone"
                    ],
                    "mon": [
                        0,
                        1,
                        2,
                        3
                    ],
                    "tue": [
                        0,
                        1,
                        2,
                        3,
                        4
                    ],
                    "wed": [
                        0,
                        1,
                        2,
                        3
                    ],
                    "thu": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5
                    ],
                    "fri": [
                        0,
                        1,
                        2,
                        3,
                        4
                    ],
                    "sat": [
                        0,
                        1,
                        2,
                        3,
                        4
                    ],
                    "sun": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6
                    ]
                },
                "pads": [
                    102643
                ],
                "mobile_types": [
                    "tablets",
                    "smartphones"
                ],
                "mobile_vendors": [],
                "mobile_operators": []
            },
            "age_restrictions": null,
            "date_start": null,
            "date_end": null,
            "autobidding_mode": "second_price_mean",
            "budget_limit_day": null,
            "budget_limit": null,
            "mixing": "fastest",
            "utm": null,
            "enable_utm": true,
            "price": "3.53",
            "max_price": "0",
            "package_id": 961,
            "banners": [
                {
                    "urls": {
                        "primary": {
                            "id": url_id
                        }
                    },
                    "textblocks": {},
                    "content": {
                        "image_240x400": {
                            "id": image_id
                        }
                    },
                    "name": ""
                }
            ]
        }
        res = self._request('POST', urljoin(self.base_url, 'api/v2/campaigns.json'), headers=headers, json=json,
                            jsonify=True)
        return res['id']

    def get_campaign_id(self, comp_id):
        resp = self._request('GET', urljoin(self.base_url, f'api/v2/campaigns.json?_id={comp_id}'), jsonify=True)
        return resp

    def post_delete_campaign(self, comp_id):
        headers = {
            'Content-Type': 'application/json',
            'referer': 'https://target.my.com/dashboard',
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }
        json = {'status': "deleted"}
        self._request('POST', urljoin(self.base_url, f'api/v2/campaigns/{comp_id}.json'), headers=headers, json=json,
                      expected_status=204)
