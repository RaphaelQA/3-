from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Namespace):

    def post(self):
        req_json = request.json

        username = req_json.get('username')
        password = req_json.get('password')

        if None in [username, password]:
            return 404

        tokens = auth_service.generate_token(username, password)

        return tokens, 201

    def put(self):
        req_json = request.json
        token = req_json.get('refresh_token')

        if token is None:
            return 400

        tokens = auth_service.refresh_token(token)

        return tokens, 201

