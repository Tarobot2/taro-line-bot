from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    StickerMessage,
    TextSendMessage,
    ImageSendMessage
)
import os
import random

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    image_url = "https://i.imgur.com/3jFhuCo.jpg"

    greeting_keywords = [
        "おはよう", "こんにちは", "こんばんは", "はじめまして", "よろしく", "hello"
    ]

    if any(keyword in user_message for keyword in greeting_keywords):
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="こんにちは！ダニエルもよろしくと言っています！"),
                TextSendMessage(text="Hi, I am Daniel. Nice to meet you."),
                ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
            ]
        )
        return

    # ✅ 天気キーワード一覧（修正済み）
    weather_keywords = [
        "天気", "天候", "気象", "空模様", "予報", "気象庁",
        "晴れ", "快晴", "晴天", "晴れる", "日差し", "太陽", "ピーカン", "陽気",
        "くもり", "曇り", "曇る", "曇天",
        "雨", "小雨", "大雨", "ゲリラ豪雨", "土砂降り", "雨降り", "降水", "梅雨", "雨模様", "にわか雨",
        "雷", "雷雨", "落雷", "かみなり",
        "雪", "大雪", "小雪", "吹雪", "雪降り", "寒波",
        "風", "強風", "突風", "台風", "暴風", "爆風", "竜巻",
        "暑い", "寒い", "蒸し暑い", "冷える", "気温", "湿度", "乾燥",
        "ざーざー", "ぽつぽつ", "じめじめ", "ゴロゴロ",
        "sunny", "fine", "clear sky", "cloudy", "overcast", "rain", "drizzle",
        "shower", "pouring", "wet", "storm", "thunder", "lightning", "snow",
        "snowfall", "blizzard", "icy", "gust", "wind", "stormy", "typhoon",
        "low pressure", "high pressure", "hot", "cold", "humid", "chill",
        "temperature", "dry", "heatwave", "weather", "forecast", "sky", "rainbow",
        "fog", "mist", "haze"
    ]

    if any(keyword in user_message for keyword in weather_keywords):
        reply = "昔は靴を飛ばして、明日の天気を予想したものです。"
    else:
        replies = [
            "バイトは楽なのが一番",
            "トレンドは同窓会マジックより消しゴムマジックですね",
            "好きな映画は「あなたが好きな映画」です。",
            "私はbotです。感情はありません。",
            "はっ倒すぞ！！！コラァ",
            "一番恐ろしいのは「有能な敵」より「なぜかなんでも知ってるご近所さん」です。",
            "直下堀りは危険です。全ロスします。",
            "早起きはくまモンの得",
            "ダニエルは人類の敵",
            "ド〜はファイトのレ〜♩",
            "屋根より低い鯉のぼり",
            "うさぎ〜まーずい〜♩かのやま〜〜　コブラ〜つ〜りし、かのかわ〜♩",
            "筋肉は裏切らない",
            "えっちなことを今考えないでください！",
            "返事がめんどくさいです",
            "「大きな栗の木の下で」って大きい栗が実っている木の下なのか、デカい木の下なのか？保育園児の時からの謎です。",
            "人間には２種類います。ローランドか、ローランドじゃないかです。",
            "I'll be back",
            "ホメロス叙事詩って褒め上手そう",
            "グッドだにょ〜ん",
            "わあ〜、おっきいですね",
            "ちっさｗ",
            "わぁ、それは悲惨だ〜",
            "太平洋と大泉洋は兄弟",
            "大西洋は大泉洋のお父さん",
            "吉田羊と大泉洋の共通点を教えて",
            "草は生えるものです"
        ]
        reply = random.choice(replies)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    replies = [
        "そのスタンプ、まだまだだな。",
        "スタンプ使いの私に太刀打ちできると思おうのか？",
        "スタンプだけで気持ち伝わるってすごくない？",
        "スタンプポンポン",
        "スタンプか、、、",
        "お前はスタンプの全てを知らない"
    ]
    reply = random.choice(replies)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
