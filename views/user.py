from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from decorators import auth_required

from implemented import user_service

user_ns = Namespace('user')

@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        user = user_service.get_all()
        res = UserSchema(many=True).dump(user)

        return res, 200


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        user = user_service.get_one(uid)
        user_schema = UserSchema().dump(user)

        return user_schema, 200

    @auth_required
    def patch(self, uid):
        req_json = request.json

        if 'id' not in req_json:
            req_json['id'] = uid

        user_service.update(req_json)

        return '', 201

    def delete(self, uid):
        user_service.delete(uid)

        return '', 204

@user_ns.route('/<int:uid>/password')
class UserView(Resource):
    def put(self, uid):
        req_json = request.json
        if 'id' not in req_json:
            req_json['id'] = uid

        user_service.update_pass(req_json)

        return 'Пароль успешно сменен', 201