from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, LocationSendMessage, FlexSendMessage, FlexContainer
import config
from Rdb import Users, SnsId, Session
from Web.Dto import ActionMessageDto

prefix = config.line_messaging_web_prefix

line_bot_api = LineBotApi(config.line_messaging_channel_access_token)
handler = WebhookHandler(config.line_messaging_channel_secret)


def send_message(user_id: str, message: str):
    messages = TextMessage(text=message)
    line_bot_api.push_message(user_id, messages)


def send_location(user_id: str, title: str, address: str, latitude: float, longitude: float):
    messages = LocationSendMessage(title, address, latitude, longitude)
    line_bot_api.push_message(user_id, messages)


def send_action_message(user_id: str, action_message: ActionMessageDto):
    # @ref https://developers.line.biz/flex-simulator/
    js = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Title",  # update
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        # insert
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                # insert
            ],
            "flex": 0
        }
    }
    [title_block, details_block] = js["body"]["contents"]
    title_block["text"] = action_message.title
    for detail in action_message.details:
        row = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": detail.label,
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": detail.text,
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                }
            ]
        }
        contents: list[dict] = details_block["contents"]
        contents.append(row)

    footer_block: list[dict] = js["footer"]["contents"]
    for k, v in action_message.actions.__dict__.items():
        if v is None:
            continue
        is_primary = k == "primary"
        t = {
            "type": "button",
            "style": "primary" if is_primary else "link",
            "height": "md" if is_primary else "sm",
            "action": {
                "type": "uri",
                "label": v.text,
                "uri": v.link
            }
        }
        footer_block.append(t)

    messages = FlexSendMessage(alt_text=action_message.title, contents=js)
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

    line_id = event.source.sender_id
    sns_id = SnsId.get_sns_id(line_id)
    if sns_id is None:
        from Java import SnsRegister
        java_response = SnsRegister.sns_register(line_id, 1)
        messages = TextMessage(
            text=f"はじめまして！ こちらから登録をお願いします！  {config.deeplink_host}/sns-register?sns_id={line_id}&token={java_response.token}")
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return
    else:
        messages = TextMessage(text=f"おかえりなさい！ アプリ起動はこちらから. {config.deeplink_host}/open")
        line_bot_api.reply_message(event.reply_token, messages=messages)
        # TODO: コマンドを処理
        return

    # messages = TextMessage(text=f"echo: {message.text = }")
    # line_bot_api.reply_message(event.reply_token, messages=messages)
