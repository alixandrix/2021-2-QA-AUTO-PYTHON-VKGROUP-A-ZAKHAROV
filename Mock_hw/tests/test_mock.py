import json
from fixtures import client, name, surname


class TestGet(object):

    def test_negative_get(self, client, name):
        resp = client.get_request(name)
        assert '404' in resp[0] and 'not found' in json.loads(resp[-1])

    def test_positive_get(self, client, name, surname):
        client.post_request(name, surname)
        resp = client.get_request(name)
        assert '200' in resp[0] and surname == json.loads(resp[-1])


class TestPost(object):

    def test_positive_post(self, client, surname, name):
        client.post_request(name, surname)
        resp = client.get_request(name)
        assert json.loads(resp[-1]) == surname

    def test_negative_post(self, client, surname, name):
        client.post_request(name, surname)
        resp = client.post_request(name, surname)
        assert '400' in resp[0] and 'already exists' in json.loads(resp[-1])


class TestPut(object):

    def test_negative_put(self, client, name, surname):
        resp = client.put_request(name, surname)
        assert '404' in resp[0] and 'not found' in json.loads(resp[-1])

    def test_positive_put(self, client, name, surname):
        client.post_request(name, surname)
        resp = client.put_request(name, surname)
        assert '201' in resp[0] and 'was updated' in json.loads(resp[-1])


class TestDelete(object):

    def test_negative_delete(self, client, name, surname):
        resp = client.delete_request(name)
        assert '404' in resp[0] and 'not found' in json.loads(resp[-1])

    def test_positive_delete(self, client, name, surname):
        client.post_request(name, surname)
        resp = client.delete_request(name)
        assert '200' in resp[0] and 'was deleted' in json.loads(resp[-1])
