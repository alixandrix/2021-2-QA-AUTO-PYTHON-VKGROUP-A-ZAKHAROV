import socket
import json
from loguru import logger


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.settimeout(0.1)
        self.client.connect((self.host, self.port))

    def receive(self):
        total_data = []
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    total_data.append(data.decode())
                else:
                    break
            except socket.timeout:
                break
        dat = ''.join(total_data).splitlines()
        logger.info(' '.join(x for x in dat))
        return dat

    def my_send(self, request):
        logger.info('\n'+ request.replace("\r", " ").replace("\n", ""))
        self.client.sendall(request.encode())

    def get_request(self, user):
        request = f'GET /get_user/{user} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.my_send(request)
        return self.receive()

    def post_request(self, user_name, user_surname):
        data = json.dumps({"name": user_name, "surname": user_surname})
        c_len = len(data.encode())
        request = f'POST /add_user HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: ' \
                  f'application/json\r\nContent-Length: {c_len}\r\n\r\n{data} '
        self.my_send(request)
        return self.receive()

    def put_request(self, user_name, user_surname):
        data = json.dumps({"name": user_name, "surname": user_surname})
        c_len = len(data.encode())
        request = f'PUT /put_surname HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: ' \
                  f'application/json\r\nContent-Length: {c_len}\r\n\r\n{data} '
        self.my_send(request)
        return self.receive()

    def delete_request(self, user):
        request = f'DELETE /delete_user/{user} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.my_send(request)
        return self.receive()