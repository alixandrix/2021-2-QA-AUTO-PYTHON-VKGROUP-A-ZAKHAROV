import uuid
import pytest


@pytest.fixture(scope='session')
def cookies(api_client):
    api_client.post_login()
    cookies_list = []
    for cookie in api_client.session.cookies:
        cookie_dict = {'domain': cookie.domain,
                       'name': cookie.name,
                       'value': cookie.value,
                       'secure': cookie.secure
                       }
        cookies_list.append(cookie_dict)

    return cookies_list


@pytest.fixture
def create_name():
    return str(uuid.uuid4())
