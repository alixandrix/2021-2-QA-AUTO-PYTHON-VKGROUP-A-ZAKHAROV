#!/usr/bin/env python3.8

import json
import os


from flask import Flask, request, jsonify
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)
WSGIRequestHandler.protocol_version = "HTTP/1.1"

SURNAME_DATA = {'A': 'B'}


@app.route('/add_user', methods=['POST'])
def create_user():
    user_name = json.loads(request.data)["name"]
    user_surname = json.loads(request.data)["surname"]
    if user_name not in SURNAME_DATA:
        SURNAME_DATA[user_name] = user_surname
        return jsonify({'user_name': user_name, 'user_surname': SURNAME_DATA[user_name]}), 200

    else:
        return jsonify(f'User_name {user_name} already exists: user_surname: {SURNAME_DATA[user_name]}'), 400

@app.route('/get_all', methods=['GET'])
def get_user_all():
        return jsonify(SURNAME_DATA), 200


@app.route('/get_user/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404


@app.route('/put_surname', methods=['PUT'])
def put_user_surname():
    user_name = json.loads(request.data)['name']
    user_surname = json.loads(request.data)['surname']
    if user_name in SURNAME_DATA:
        SURNAME_DATA.update({user_name: user_surname})
        return jsonify(f'Surname for user "{user_name}" was updated on "{user_surname}"'), 201
    else:
        return jsonify(f'User "{user_name}" not found'), 404

@app.route('/delete_user/<name>', methods=['DELETE'])
def delete_user(name):
    try:
        del SURNAME_DATA[name]
        return jsonify(f'User "{name}" was deleted'), 200
    except KeyError:
        return jsonify(f'User "{name}" not found'), 404




if __name__ == '__main__':
    host = os.environ.get('MOCK_HOST', '127.0.0.1')
    port = os.environ.get('MOCK_PORT', '5000')

    app.run(host, port)
