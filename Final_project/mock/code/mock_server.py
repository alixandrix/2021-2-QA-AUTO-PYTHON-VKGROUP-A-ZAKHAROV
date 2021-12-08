#!/usr/bin/env python3.8
import os

from flask import Flask, jsonify
from client import MysqlORMClient

app = Flask(__name__)

client = MysqlORMClient()


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    vk_id = client.get_vk_id(username=username)
    if vk_id:
        return jsonify({"vk_id": vk_id.id}), 200
    else:
        client.put_vk_id(username=username)
        return jsonify(), 404


@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": 'OK'}), 200


if __name__ == '__main__':
    host = os.environ['MOCK_HOST']
    port = os.environ['MOCK_PORT']
    app.run(host, int(port))
