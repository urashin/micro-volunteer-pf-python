from flask import Flask, request, jsonify
import config
from . import Dto
from .LineMessaging import send_message, send_location, send_action_message
from linebot.exceptions import LineBotApiError

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

        @app.route(f"{prefix}/send-text", methods=["POST"])
        def send_text():
            params = request.json
            try:
                req = Dto.SendTextRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            try:
                send_message(req.sns_id, message=req.message)
            except LineBotApiError as e:
                s = f"LineBotApiError: status: {e.status_code}, message: {e.message}"
                return error_response(s)

            cls = Dto.SendTextResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(
                ),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200

        @app.route(f"{prefix}/send-location", methods=["POST"])
        def send_location_message():
            params = request.json
            try:
                req = Dto.SendLocationRequest(**params)
            except TypeError as e:
                return error_response(str(e))

            try:
                send_location(req.sns_id, req.title, req.address, req.latitude, req.longitude)
            except LineBotApiError as e:
                s = f"LineBotApiError: status: {e.status_code}, message: {e.message}"
                return error_response(s)

            cls = Dto.SendLocationResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(
                ),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200

        @app.route(f"{prefix}/send-request-volunteer", methods=["POST"])
        def send_request_volunteer():
            params = request.json
            try:
                req = Dto.SendRequestVolunteerRequest.from_json(params)
            except TypeError as e:
                return error_response(str(e))

            try:
                send_location(req.sns_id, req.location_message.title, req.location_message.address,
                              req.location_message.latitude, req.location_message.longitude)
            except LineBotApiError as e:
                s = f"LineBotApiError[send_location]: status: {e.status_code}, message: {e.message}"
                return error_response(s)

            try:
                send_action_message(req.sns_id, req.action_message)
            except LineBotApiError as e:
                s = f"LineBotApiError[send_action_message]: status: {e.status_code}, message: {e.message}"
                return error_response(s)

            cls = Dto.SendRequestVolunteerResponse
            res = {
                "status": 200,
                "message": "ok",
                "response": cls(
                ),
            }
            res2: Dto.BaseResponse[cls] = Dto.BaseResponse(**res)

            return jsonify(res2), 200
