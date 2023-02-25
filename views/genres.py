from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from decorators import admin_required, auth_required
from implemented import genre_service
from parsers import page_parser

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    # @auth_required
    def get(self):
        filters = page_parser.parse_args()
        rs = genre_service.get_all(filters)
        res = GenreSchema(many=True).dump(rs)
        return res, 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @auth_required
    def put(self, gid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = gid
        genre_service.update(req_json)
        return "", 204

    @auth_required
    def delete(self, gid):
        genre_service.delete(gid)
        return "", 204
