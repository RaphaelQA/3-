from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

auth_ns = Namespace('auth')

@auth_ns.route('/register')
class AuthRegView(Resource):

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)

        return '', 201, {'location': f'/users/{user.id}'}

@auth_ns.route('/login')
class AuthRegView(Resource):
    def post(self):
        req_json = request.json

        email = req_json.get('email')
        password = req_json.get('password')

        if None in [email, password]:
            return 404

        tokens = auth_service.generate_token(email, password)

        return tokens, 201

    def put(self):
        req_json = request.json
        token = req_json.get('refresh_token')

        if token is None:
            return 400

        tokens = auth_service.refresh_token(token)

        return tokens, 201


