from flask import Flask, request, abort
import requests
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('tAjDgY5CeROGSM2ldUxOVCtBZ2mkTlHWsYHgSbTCWngIrUIMJCAR7dTPNEJDuyapwF31Z6HEdEomgNK3Fno+ZLu0ljGEuwY3nZb1i7+Zopk6huskXf4OSZ4Nz2MJrBmul3ysNt/qBrXErzPcSZDzOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('80530a6fcbe0137d29e2b63939e3b391')


@app.route("/callback", methods=['POST'])
def callback():
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
def handle_message(event):
    # リプライを作成する
    reply = create_reply(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        # 実際にcreate_replyの返り値をTextMessageの引数として渡してます。
        TextSendMessage(text=event.message.text))

def create_reply(user_text):
    apikey = "DZZ4WiCatLM5WuZCR6OgE7SMonUoJhA7"
    talk_url = "https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"
    payload = {"apikey": apikey, "query": user_text}
    res = requests.post(talk_url, data=payload).json()

    return res['results'][0]['reply']


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
    app.run()
