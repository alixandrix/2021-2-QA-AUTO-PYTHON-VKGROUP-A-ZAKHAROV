import os
import signal
import subprocess
import time
from copy import copy
import requests
from requests.exceptions import ConnectionError

import settings

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 5s!')


def pytest_configure(config):

    if not hasattr(config, 'workerinput'):

        mock_path = os.path.join(repo_root, 'mock_server', 'mock_server.py')

        env = copy(os.environ)
        env.update({
            'MOCK_HOST': settings.MOCK_HOST,
            'MOCK_PORT': settings.MOCK_PORT

        })

        mock_stderr = open('/tmp/mock_stderr', 'w')
        mock_stdout = open('/tmp/mock_stdout', 'w')

        mock_proc = subprocess.Popen(['python3.8', mock_path],
                                    stderr=mock_stderr, stdout=mock_stdout,
                                    env=env)
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)

        config.mock_proc = mock_proc
        config.mock_stderr = mock_stderr
        config.mock_stdout = mock_stdout


def pytest_unconfigure(config):
    config.mock_proc.send_signal(signal.SIGINT)
    exit_code = config.mock_proc.wait()

    assert exit_code == 0, f'app exited abnormally with exit code: {exit_code}'

    config.mock_stderr.close()
    config.mock_stdout.close()



