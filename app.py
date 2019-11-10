from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from fuzzywuzzy import process
from yandex.Translater import Translater

app = Flask(__name__)

line_bot_api = LineBotApi('6S/g+yViNJKdD5J1k7/keFYiYNDrRckl+XSlT9o2DKuXz0fcz5F9QSz2671cDQikXcT8DSypjmkp/H/XG00/d1JdoRKHG3vauMDw1lAYKN+idfiy1P76DGCjMQXr4kUEPEuOhIcDY72GMQMTik37/wdB04t89/1O/w1cDnyilFU=/')
handler = WebhookHandler('227b1d64bc0b475565d50a947d79504b')
user_session = {}
tr = Translater()
tr.set_key('trnsl.1.1.20191110T032857Z.5cb504ab3196bc0f.e222fb57077985f5bc174f9f7b8ff5622b83d7ed') # Api key found on https://translate.yandex.com/developers/keys


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

from yandex.Translater import Translater
# tr = Translater()
# # tr.set_key('trnsl.1.1.20191108T161057Z.789702196707e5b2.41eba9a721c3e06bd2ae57a2a1189764eb9e1b8d') # Api key found on https://translate.yandex.com/developers/keys
# tr.set_key('trnsl.1.1.20191110T032857Z.5cb504ab3196bc0f.e222fb57077985f5bc174f9f7b8ff5622b83d7ed') # Api key found on https://translate.yandex.com/developers/keys
# tr.set_from_lang('en')
# tr.set_to_lang('th')
# # tr.set_text('Where is thailand?')
# # new = tr.translate()
# # print(new)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    text_from_user = event.message.text
    # tr.set_text(text_from_user)
    # new = tr.translate()
    # text_to_send = TextSendMessage(text=new)

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     text_to_send
    # )

    print(event)

    replytoken = event.reply_token
    userid = event.source.user_id
    user_current_session = user_session[userid]['session']

    # if user_current_session == None and text_from_user == 'แปลข้อความ':
    if text_from_user == 'แปลข้อความ':
        action1 = MessageAction(label="English", text="English")
        qbtn1 = QuickReplyButton(action=action1)
        action2 = MessageAction(label="France", text="France")
        qbtn2 = QuickReplyButton(action=action2)
        action3 = MessageAction(label="German", text="German")
        qbtn3 = QuickReplyButton(action=action3)
        action4 = MessageAction(label="Japan", text="Japan")
        qbtn4 = QuickReplyButton(action=action4)

        qreply = QuickReply(items=[qbtn1, qbtn2, qbtn3, qbtn4])
        
        text = TextSendMessage(text="ต้องการแปลเป็นภาษาอะไรคะ?", quick_reply=qreply)
        line_bot_api.reply_message(replytoken, text)
        user_session[userid]['session'] = "Selectlang"
    elif user_current_session == "Selectlang":
        from translator import check_lang
        True_lang = check_lang(Input=text_from_user)
        if True_lang is None:
            text = TextSendMessage(text="ไม่สามารถแปลได้ กรุณาเลือกภาษาใหม่อีกครั้ง")
            line_bot_api.reply_message(replytoken, text)
        else:
            text = TextSendMessage(text="ท่านต้องการให้ดิฉันแปลจาก ไทย เป็น {} ใช่ไหมคะ".format(True_lang))
            text2 = TextSendMessage(text="กรุณาพิมพ์ข้อความที่ต้องการแปล")
            line_bot_api.reply_message(replytoken, messages=[text, text2])
            user_session[userid]['session'] = "textinput"
            user_session[userid]['lang'] = True_lang

    elif user_current_session == "textinput":
        from translator import tran
        output = tran(text_from_user=text_from_user, to_lang=user_session[userid]['lang'], tr=tr)
        
        from Flex import Flex_output
        flex_to_reply = Flex_output(text=output)
        flex_object = Base.get_or_new_from_json_dict(flex_to_reply, FlexSendMessage)
        line_bot_api.reply_message(replytoken, messages=flex_object)
        user_session[userid]['session'] = "continue"

    elif user_current_session == "continue":
        if text_from_user == 'แปลข้อความใหม่':
            text2 = TextSendMessage(text="กรุณาพิมพ์ข้อความที่ต้องการแปล")
            line_bot_api.reply_message(replytoken, messages=text2)
            user_session[userid]['session'] = "textinput"
        elif text_from_user == 'แปลข้อความใหม่':
            text2 = TextSendMessage(text="ขอบคุณที่ใช้บริการคะ")
            line_bot_api.reply_message(replytoken, messages=text2)
            user_session[userid]['session'] = None
        
@handler.add(FollowEvent)
def Greeting(event):
    userid = event.source.user_id # get userid
    user = {}
    user['session'] = None
    user['lang'] = None
    user_session[userid] = user

    line_bot_api.link_rich_menu_to_user(user_id=userid, rich_menu_id="richmenu-4c03da50fb2d273a2abe1445dcd17e0e")

    text = TextSendMessage(text="สวัสดีคะ ยินดีต้อนรับสู่บริการแปลข้อความ")
    reply_tok = event.reply_token
    line_bot_api.reply_message(reply_tok,messages=text) ##ตอบกลับ

import os
@app.route('/<picname>')
def getimage(picname):
    current_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(current_path, 'pic', 'pic1')
    return send_from_directory(dir_path, picname)

@app.route('/<picname>/1040')
def getimagemap(picname):
    current_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(current_path, 'pic', 'pic1')
    return send_from_directory(dir_path, picname)

if __name__ == "__main__":
    app.run(port=8000)