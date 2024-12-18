import os
from argparse import ArgumentParser
from flask import (
    Flask,
    request,
    abort
)
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

from predict import Predictor


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
    received_message = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name
    reply = f'{display_name}さんのメッセージ\n{received_message}'
    line_bot_api.reply_message(ReplyMessageRequest(
        replyToken=event.reply_token,
        messages=[TextMessage(text=reply)]
    ))


@app.route('/', methods=['GET'])
def toppage():
    return 'Hello world!'


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '--local',
        action='store_true',
        help='train models with local data'
    )
    args = parser.parse_args()

    if args.local:
        print('run local')
    else:
        print('run online')
        # app.run(host="0.0.0.0", port=8000, debug=True)
