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

@app.route("/", methods=['GET'])
def ping():
    return "Taro Bot is awake!"

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
    print(f"[DEBUG] user_message: {user_message}")

    image_url = "https://i.imgur.com/3jFhuCo.jpg"

    greeting_keywords = ["おはよう", "こんにちは", "こんばんは", "はじめまして", "よろしく", "hello"]
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

    weather_keywords = ["天気", "雨", "晴れ", "曇り", "雷", "雪", "気温", "風", "台風"]
    if any(keyword in user_message for keyword in weather_keywords):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="昔は靴を飛ばして、明日の天気を予想したものです。")
        )
        return

    fitness_keywords = ["筋肉", "運動", "トレーニング", "プロテイン", "ジム", "鍛える"]
    love_keywords = ["恋", "好き", "告白", "振られた", "LINEこない", "彼女", "彼氏","恋愛","愛","浮気","男友達","女友達"]
    otaku_keywords = ["アニメ", "ゲーム", "推し", "イベント", "オタク","推し活","アイドル","オープニング","エンディング"]
    philosophy_keywords = ["人生", "意味", "虚無", "死にたい", "考えすぎ","哲学","深い"]
    nonsense_keywords = ["あああ", "ｷﾞｬｰ", "うおおお", "！！", "意味不明", "叫び","クァwせdrftgyﾌｼﾞｺlp","ttっ"]

    fitness_replies = [
        "筋肉モリモリマッチョマンのへ〜んたいだ。",
        "なかやまきんに君は私の先輩です。",
        "鬼の背中＆背中のクリスマスツリー。世界観どうなっとるん？",
        "人間は裏切る。筋肉は裏切らない。つまり、裏切り者をジムに連れていけば改心するはずです。",
        "ダンベル落としたら床が泣いた。"
    ]

    love_replies = [
        "おい、やめろ。リア充",
        "イオンでイチャイチャするようなカップルにはなりたくない。",
        "恋愛相談は別料金です。10分15000円から",
        "それは間違いです。",
        "君が好きです。付き合ってほしいな"
    ]

    otaku_replies = [
        "推しは死なないやつを選べ。",
        "アキバに行こう！。",
        "真のオタクはオタクみたいな格好してる",
        "エヴァになりたい",
        "オープニングでジャンプするアニメは神アニメ。"
    ]

    philosophy_replies = [
        "感情を感じよう。",
        "魂をアップロードしよう！。",
        "哲学、それはすべての基礎！！",
        "脳にアプデきました！よ！！！。",
        "お前は敵の敵だ！！"
    ]

    nonsense_replies = [
        "ｳﾜｰｰｰｯ‼︎（音割れ）",
        "チャレンジでやったところだ！。",
        "広辞苑に載せたい言葉、第13位！",
        "読める、読めるぞ！！",
        "こ、これは……古代バビロニア語！？"
    ]

    default_replies = [
        "ふーん……？",
        "この情報を冷蔵庫に貼っときます。",
        "脳の回転を早めることで、さらにバカになる",
        "豆腐の角で頭打ってみて",
        "可愛いだけじゃダメに決まっとるやろ！！。",
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

    if any(keyword in user_message for keyword in fitness_keywords):
        reply = random.choice(fitness_replies)
    elif any(keyword in user_message for keyword in love_keywords):
        reply = random.choice(love_replies)
    elif any(keyword in user_message for keyword in otaku_keywords):
        reply = random.choice(otaku_replies)
    elif any(keyword in user_message for keyword in philosophy_keywords):
        reply = random.choice(philosophy_replies)
    elif any(keyword in user_message for keyword in nonsense_keywords):
        reply = random.choice(nonsense_replies)
    else:
        reply = random.choice(default_replies)

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
