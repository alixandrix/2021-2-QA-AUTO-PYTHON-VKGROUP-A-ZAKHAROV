import logging
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


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

    @property
    def post_headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': 'https://target.my.com/',

        }

    @staticmethod
    def log_pre(url, headers, data, expected_status):
        logger.info(f'Performing request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
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

    def _request(self, method, url, headers=None, data=None, expected_status=200, jsonify=False, json=None):
        self.log_pre(url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, json=json)
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
        headers = self.post_headers
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
                      'https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags',
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
        return self._request('DELETE', urljoin(self.base_url, f'api/v2/remarketing/segments/{id_segment}.json'), headers=headers, expected_status=204)

    def post_create_campaign(self, name_campaign):
        headers = {
            'Content-Type': 'application/json',
            'referer': 'https://target.my.com/campaign/new',
            'X-Campaign-Create-Action': 'new',
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        }

        json = {
  "name": name_campaign,
  "read_only": 'false',
  "conversion_funnel_id": 'null',
  "objective": "traffic",
  "enable_offline_goals": 'false',
  "targetings": {
    "split_audience": [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10
    ],
    "sex": [
      "male",
      "female"
    ],
    "age": {
      "age_list": [
        0,
        12
      ],
      "expand": 'true'
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
      "mon": [0],
      "tue": [0, 1],
      "wed": [
        0,
        1,
        2],
      "thu": [
        0,
        1,
        2,
        3
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
        4,
        5
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
  "age_restrictions": 'null',
  "date_start": 'null',
  "date_end": 'null',
  "autobidding_mode": "second_price_mean",
  "budget_limit_day": 'null',
  "budget_limit": 'null',
  "mixing": "fastest",
  "utm": 'null',
  "enable_utm": 'true',
  "price": "3.61",
  "max_price": "0",
  "package_id": 961,
  "banners": [
    {
      "urls": {
        "primary": {
          "id": 1321805
        }
      },
      "textblocks": {},
      "content": {
        "image_240x400": {
          "id": 9690429
        }
      },
      "name": ""
    }
  ]
}
        res = self._request('POST', urljoin(self.base_url, 'api/v2/campaigns.json'), headers=headers, json=json, jsonify=True, expected_status=400)
        print(res)
        return res