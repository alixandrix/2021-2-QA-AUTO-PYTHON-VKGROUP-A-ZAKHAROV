
from client.client import *
import settings

def test_get():
    cl = Client(settings.MOCK_HOST, settings.MOCK_PORT)
    cl.connect()
    b = cl.get_request('A')
    assert json.loads(b[-1]) == "B"

def test_post():
    cl = Client(settings.MOCK_HOST, settings.MOCK_PORT)
    cl.connect()
    cl.post_request('Amma', 'Pols')
    b = cl.get_request('Amma')
    assert json.loads(b[-1]) == "Pols"

def test_put():
    cl = Client(settings.MOCK_HOST, settings.MOCK_PORT)
    cl.connect()
    cl.put_request('A', 'P')
    b = cl.get_request('A')
    assert json.loads(b[-1]) == "P"

def test_delete():
    cl = Client(settings.MOCK_HOST, settings.MOCK_PORT)
    cl.connect()
    cl.delete_request('A')
    b = cl.get_request('A')
    assert 'not found' in json.loads(b[-1])

