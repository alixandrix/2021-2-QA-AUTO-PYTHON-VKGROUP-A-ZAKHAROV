import socket
import json


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.settimeout(0.1)
        self.client.connect((self.host, self.port))

    def recieve(self):
        total_data = []
        while True:
            data = self.client.recv(4096)
            print(f'received data: {data}')
            if data:
                total_data.append(data.decode())
            else:
                break
        dat = ''.join(total_data).splitlines()
        return dat

    def recieve2(self):
        total_data = []
        while True:
            try:
                data = self.client.recv(1024)
                print(f'received data: {data}')
                if data:
                    total_data.append(data.decode())
                else:
                    break
            except socket.timeout:
                break
        dat = ''.join(total_data).splitlines()
        return dat

    def get_request(self, user):
        request = f'GET /get_user/{user} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.client.sendall(request.encode())
        return self.recieve2()

    def post_request(self, user_name, user_surname):
        data = json.dumps({"name": user_name, "surname": user_surname})
        c_len = len(data.encode())
        request = f'POST /add_user HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: ' \
                  f'application/json\r\nContent-Length: {c_len}\r\n\r\n{data} '
        self.client.send(request.encode())
        return self.recieve2()

    def put_request(self, user_name, user_surname):
        data = json.dumps({"name": user_name, "surname": user_surname})
        c_len = len(data.encode())
        request = f'PUT /put_surname HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: ' \
                  f'application/json\r\nContent-Length: {c_len}\r\n\r\n{data} '
        self.client.send(request.encode())
        return self.recieve2()

    def delete_request(self, user):
        request = f'DELETE /delete_user/{user} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.client.sendall(request.encode())
        return self.recieve2()