import os
from argparse import ArgumentParser
from flask import Flask, request, abort
import time

from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    PostbackAction
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    PostbackEvent,
    TextMessageContent
)

from commuter.model import Predictor


load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

app = Flask(__name__)

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature."
            "Please check your channel access token/channel secret."
        )
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    user_id = event.source.user_id
    received_message = event.message.text

    # メッセージを受け取ってパース
    #  - メッセージ中に「出発」に関連する言葉があるか
    #  - メッセージ中に「到着」に関連する言葉があるか

    # 「出発」があれば，現在時刻とともにBordingリストに追加
    #  - ユーザに対応するモデルが存在すれば，現在時刻を入力に予測到着時刻を返信
    # 「到着」があれば，Bordingリストから検索
    #  - いれば，記録された出発時刻と現在時刻の差をとる
    #    - 差が90m以上ならばスキップ，更新しなかった旨を返信
    #    - 差が90m以内ならばモデルを更新，更新の旨を返信

    user_name = line_bot_api.get_profile(user_id).display_name
    reply = f'{user_name}さん（ID：{user_id}）のメッセージ\n{received_message}'
    line_bot_api.reply_message(ReplyMessageRequest(
        replyToken=event.reply_token,
        messages=[TextMessage(text=reply)]
    ))


@app.route('/', methods=['GET'])
def toppage():
    return 'Hello world!'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
