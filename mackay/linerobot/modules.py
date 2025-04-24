import json
import re
import environ
import os

from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# pip install line-bot-sdk

# QuickReplyButton, MessageAction, messages ,events
from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage

from .models import user_linebot_track
# from linebot.models import actions
# from linebot.models import template
# from linebot.models.actions import URIAction
# from linebot.models.send_messages import AudioSendMessage, VideoSendMessage

env = environ.Env()
environ.Env.read_env()
LINE_CHANNEL_ACCESS_TOKEN = env('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
print('LINE_CHANNEL_ACCESS_TOKEN', LINE_CHANNEL_ACCESS_TOKEN)


def start_epro(event, lindId):
    try:
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": f"https://storage.googleapis.com/wdcare-file-storage/static/img/trm01.63651c88.png",
                        "size": "full",
                        "aspectRatio": "13:9",
                        "aspectMode": "cover",
                    },
                    {
                        "type": "text",
                        "text": "歡迎加入Wdcare傷口照護",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "「Wdcare」為傷口照護平台，提供精準個人化的數位療法與癌症預防，解決病患出院回家後求助無門的問題。",
                        "size": "sm",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "開始作答",
                            "data": "action=start"
                        }
                    },
                    # {
                    #     "type": "button",
                    #     "style": "primary",
                    #     "action": {
                    #         "type": "postback",
                    #         "label": "更多介紹",
                    #         "data": "action=more_info"
                    #     }
                    # }
                ]
            }
        }

        flex_message = FlexSendMessage(
            alt_text="歡迎加入Wdcare傷口照護",
            contents={
                "type": "carousel",
                "contents": [bubble]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))


def start_epro_ques_1(event, lindId):
    try:
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "【問題1】您是否有頭暈嘔吐現象?",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "這裡放輔助說明的小字",
                        "size": "sm",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "有",
                            "data": "action=epro1,有"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "沒有",
                            "data": "action=epro1,沒有"
                        }
                    },
                ]
            }
        }

        flex_message = FlexSendMessage(
            alt_text="症狀問題1",
            contents={
                "type": "carousel",
                "contents": [bubble]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))


def start_epro_ques_2(event, lindId):
    try:
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "【問題2】您最近3天有腹瀉程度?",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "這裡放輔助說明的小字",
                        "size": "sm",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "沒有",
                            "data": "action=epro2,沒有"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "普通",
                            "data": "action=epro2,普通"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "超嚴重",
                            "data": "action=epro2,超嚴重"
                        }
                    },
                ]
            }
        }

        flex_message = FlexSendMessage(
            alt_text="症狀問題1",
            contents={
                "type": "carousel",
                "contents": [bubble]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))



def clean_epro_answer(text):
    splitString = text.split(',')
    print('\033[93m' + f'splitString: {splitString}' + '\033[0m')
    category = splitString[0].replace('action=', '')

    if len(splitString) > 1:
        reply = splitString[1]
    else:
        reply = ''

    print('splitString 2 ', category, reply)
    print('\033[93m' + f'splitString Transform: {category}, {reply}' + '\033[0m')
    return category, reply


def handle_postback(event):
    data = event.postback.data
    lineId = event.source.user_id
    print('\033[93m' + f'handle_postback: {event.postback}' + '\033[0m')
    category, reply = clean_epro_answer(data)

    if category == 'start':
        start_epro_ques_1(event, data)

    elif category == 'epro1':
        start_epro_ques_2(event, data)
        user_linebot_track.objects.create(
            line_id = lineId,
            request = reply,
            category = category)

    elif category == 'epro2':
        user_linebot_track.objects.create(
            line_id = lineId,
            request = reply,
            category = category)
        
        message = TextSendMessage(text='作答完畢，感謝配合')
        line_bot_api.reply_message(event.reply_token, message)
   
    else:
        message = TextSendMessage(text='發生錯誤!')
        line_bot_api.reply_message(event.reply_token, message)
