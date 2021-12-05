from flask import Flask, request, jsonify
import config
from . import Dto
from Rdb import Users, SnsId, Session
from .LineMessaging import send_message

prefix = config.api_web_prefix


def error_response(message: str, status: int = 400, http_status: int = 400):
    res = {
        "status": status,
        "message": message,
        "response": None,
    }
    res2 = Dto.BaseResponse[None](**res)
    return jsonify(res2), http_status


class Api:
    def __init__(self, app: Flask):
        self.app = app

        @app.route(f"{prefix}/create", methods=["POST"])
        def create():
            params = request.json
            try:
                req = Dto.UserCreateRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            from uuid import uuid4
            session_id = uuid4().hex
            Users.set_user(req.user_id, req.password, req.name, f"{req.user_id}@tokyo.oss")
            Session.set_session(session_id, req.user_id)

            cls = Dto.UserCreateResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(
                    user_id=req.user_id,
                    token=session_id,
                ),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200

        @app.route(f"{prefix}/login", methods=["POST"])
        def login():
            params = request.json
            try:
                req = Dto.LoginRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            user = Users.get_user(req.user_id)
            if user is None or user.password != req.password:
                return error_response("user/password incorrect")

            session = Session.get_session_by_user_id(req.user_id)
            token = session.session_id

            cls = Dto.LoginResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(
                    token=token,
                ),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200

        @app.route(f"{prefix}/login-info", methods=["POST"])
        def login_info():
            params = request.json
            try:
                req = Dto.LoginInfoRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            session = Session.get_session(req.token)
            if session is None:
                return error_response("invalid token")
            user = Users.get_user(session.user_id)
            if user is None:
                return error_response("invalid token. user does not exists")

            cls = Dto.LoginInfoResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(
                    user_id=user.user_id,
                    name=user.name,
                    email=user.email,
                ),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200

        @app.route(f"{prefix}/link-sns", methods=["POST"])
        def link_sns():
            params = request.json
            try:
                req = Dto.LinkSnsRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            session = Session.get_session(req.token)
            if session is None:
                return error_response("invalid token")
            SnsId.set_sns_id(req.sns_id, session.user_id)

            cls = Dto.LinkSnsResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200

        @app.route(f"{prefix}/sns-greet", methods=["POST"])
        def sns_greet():
            params = request.json
            try:
                req = Dto.SnsGreetRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            session = Session.get_session(req.token)
            if session is None:
                return error_response("invalid token")
            user = Users.get_user(session.user_id)

            sns_ids = SnsId.get_all_sns_id()
            for sns_id in sns_ids:
                send_message(sns_id.sns_id, f"{user.name}さんからgreet: {req.message}")

            cls = Dto.SnsGreetResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200
