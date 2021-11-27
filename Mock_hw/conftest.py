import os
import shutil
import signal
import subprocess
import sys
import time
from copy import copy
import requests
from requests.exceptions import ConnectionError
import settings
from loguru import logger



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
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        os.makedirs(base_dir)
        mock_path = os.path.join(repo_root, 'mock_server', 'mock_server.py')
        env = copy(os.environ)
        env.update({
            'MOCK_HOST': settings.MOCK_HOST,
            'MOCK_PORT': settings.MOCK_PORT

        })

        mock_stderr = open(os.path.join(base_dir, 'mock_stderr'), 'w')
        mock_stdout = open(os.path.join(base_dir, 'mock_stdout'), 'w')

        mock_proc = subprocess.Popen(['python3.8', mock_path],
                                     stderr=mock_stderr, stdout=mock_stdout,
                                     env=env)
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)

        config.mock_proc = mock_proc
        config.mock_stderr = mock_stderr
        config.mock_stdout = mock_stdout
    config.base_temp_dir = base_dir
    logger.remove()
    logger.add(os.path.join(base_dir, 'file.log'), format="{message}",
               level='INFO',
               colorize=True)


def pytest_unconfigure(config):
    config.mock_proc.send_signal(signal.SIGINT)
    exit_code = config.mock_proc.wait()

    assert exit_code == 0, f'app exited abnormally with exit code: {exit_code}'

    config.mock_stderr.close()
    config.mock_stdout.close()

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))
