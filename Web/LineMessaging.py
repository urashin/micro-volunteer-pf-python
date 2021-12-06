from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import config
# from Db import Users, SnsId
from Rdb import Users, SnsId, Session

prefix = config.line_messaging_web_prefix

line_bot_api = LineBotApi(config.line_messaging_channel_access_token)
handler = WebhookHandler(config.line_messaging_channel_secret)


def send_message(user_id: str, message: str):
    messages = TextMessage(text=message)
    line_bot_api.push_message(user_id, messages)


class LineMessaging:
    def __init__(self, app: Flask):
        self.app = app

        # https://qiita.com/kotamatsuoka/items/c4e651f1cb6c4490f4b8

        @app.route(f"{prefix}/callback", methods=["POST"])
        def line_messaging_callback():
            # get X-Line-Signature header value
            signature = request.headers['X-Line-Signature']

            # get request body as text
            body = request.get_data(as_text=True)
            app.logger.info("Request body: " + body)

            # handle webhook body
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                print("Invalid signature. Please check your channel access token/channel secret.")
                abort(400)

            return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def response_message(event: MessageEvent):
    message = event.message
    if not isinstance(message, TextMessage):
        return
    command = message.text.lower().strip()
    try:
        if command.startswith("create"):
            arg = command.split(" ")[1:]
            user_id, password, name = arg
            # Users.create_user(user_id, password, name)
            # SnsId.insert_sns(user_id, event.source.sender_id, "LINE")
            from uuid import uuid4
            session_id = uuid4().hex
            sns_id = event.source.sender_id
            Users.set_user(user_id, password, name, f"{user_id}@example.com")
            Session.set_session(session_id, user_id)
            SnsId.set_sns_id(sns_id, user_id)

            line_bot_api.reply_message(event.reply_token,
                                       messages=TextMessage(text=f"user `{user_id}` created"))
            return

        elif command.startswith("login"):
            arg = command.split(" ")[1:]
            user_id, password = arg
            # token = Users.login(user, password)
            user = Users.get_user(user_id)
            if user is None or user.password != password:
                raise Exception("password incorrect")
            session = Session.get_session_by_user_id(user_id)
            token = session.session_id
            line_bot_api.reply_message(event.reply_token,
                                       messages=TextMessage(text=f"logged in `{token}`"))
            return

        elif command.startswith("greet"):
            arg = command.split(" ")[1:]
            token = arg.pop(0)
            # user = Users.get_user_by_token(token)
            # if user is None:
            #     line_bot_api.reply_message(event.reply_token,
            #                                messages=TextMessage(text="invalid token"))
            #     return
            #
            text = " ".join(arg)
            # sns_ids = SnsId.get_all_sns_by_type("LINE")
            # for sns_id in sns_ids:
            #     send_message(sns_id.sns_id, f"{user.name}さんからbroadcast: {text}")
            session = Session.get_session(token)
            if session is None:
                raise Exception("invalid session")
            user = Users.get_user(session.user_id)
            sns_ids = SnsId.get_all_sns_id()
            for sns_id in sns_ids:
                send_message(sns_id.sns_id, f"{user.name}さんからbroadcast: {text}")
            return

    except Exception as e:
        import traceback
        traceback.format_exc()
        line_bot_api.reply_message(event.reply_token,
                                   messages=TextMessage(text="command error: " + str(e)))
        return

    line_id = event.source.sender_id
    sns_id = SnsId.get_sns_id(line_id)
    if sns_id is None:
        from Java import SnsRegister
        java_response = SnsRegister.sns_register(line_id, 1)
        messages = TextMessage(text=f"はじめまして！ こちらから登録をお願いします！  {config.deeplink_host}/sns-register?sns_id={line_id}&token={java_response.token}")
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return
    else:
        messages = TextMessage(text=f"おかえりなさい！ アプリ起動はこちらから. {config.deeplink_host}/open")
        line_bot_api.reply_message(event.reply_token, messages=messages)
        # TODO: コマンドを処理
        return

    # messages = TextMessage(text=f"echo: {message.text = }")
    # line_bot_api.reply_message(event.reply_token, messages=messages)
