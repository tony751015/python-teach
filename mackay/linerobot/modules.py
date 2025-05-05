import json
import re
import environ
import os

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
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


# def start_epro_ques_1(event, lindId):
#     try:
#         bubble = {
#             "type": "bubble",
#             "body": {
#                 "type": "box",
#                 "layout": "vertical",
#                 "contents": [
#                     {
#                         "type": "text",
#                         "text": "【問題1】您是否有頭暈嘔吐現象?",
#                         "weight": "bold",
#                         "size": "lg"
#                     },
#                     {
#                         "type": "text",
#                         "text": "這裡放輔助說明的小字",
#                         "size": "sm",
#                         "wrap": True,
#                         "margin": "md"
#                     }
#                 ]
#             },
#             "footer": {
#                 "type": "box",
#                 "layout": "vertical",
#                 "spacing": "sm",
#                 "contents": [
#                     {
#                         "type": "button",
#                         "style": "primary",
#                         "action": {
#                             "type": "postback",
#                             "label": "有",
#                             "data": "action=epro1,有"
#                         }
#                     },
#                     {
#                         "type": "button",
#                         "style": "primary",
#                         "action": {
#                             "type": "postback",
#                             "label": "沒有",
#                             "data": "action=epro1,沒有"
#                         }
#                     },
#                 ]
#             }
#         }

#         flex_message = FlexSendMessage(
#             alt_text="症狀問題1",
#             contents={
#                 "type": "carousel",
#                 "contents": [bubble]
#             }
#         )
#         line_bot_api.reply_message(event.reply_token, flex_message)
#     except Exception as e:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))


# def start_epro_ques_2(event, lindId):
#     try:
#         bubble = {
#             "type": "bubble",
#             "body": {
#                 "type": "box",
#                 "layout": "vertical",
#                 "contents": [
#                     {
#                         "type": "text",
#                         "text": "【問題2】您最近3天有腹瀉程度?",
#                         "weight": "bold",
#                         "size": "lg"
#                     },
#                     {
#                         "type": "text",
#                         "text": "這裡放輔助說明的小字",
#                         "size": "sm",
#                         "wrap": True,
#                         "margin": "md"
#                     }
#                 ]
#             },
#             "footer": {
#                 "type": "box",
#                 "layout": "vertical",
#                 "spacing": "sm",
#                 "contents": [
#                     {
#                         "type": "button",
#                         "style": "primary",
#                         "action": {
#                             "type": "postback",
#                             "label": "沒有",
#                             "data": "action=epro2,沒有"
#                         }
#                     },
#                     {
#                         "type": "button",
#                         "style": "primary",
#                         "action": {
#                             "type": "postback",
#                             "label": "普通",
#                             "data": "action=epro2,普通"
#                         }
#                     },
#                     {
#                         "type": "button",
#                         "style": "primary",
#                         "action": {
#                             "type": "postback",
#                             "label": "超嚴重",
#                             "data": "action=epro2,超嚴重"
#                         }
#                     },
#                 ]
#             }
#         }

#         flex_message = FlexSendMessage(
#             alt_text="症狀問題1",
#             contents={
#                 "type": "carousel",
#                 "contents": [bubble]
#             }
#         )
#         line_bot_api.reply_message(event.reply_token, flex_message)
#     except Exception as e:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))

def generate_question_card(event, ques_no, ques, detail, foot_btn):
    """
    動態生成問題字卡
    :param event: LINE Bot 事件
    :param ques_no: 問題編號
    :param ques: 問題文字
    :param detail: 輔助說明文字
    :param foot_btn: 按鈕列表，每個按鈕包含 label 和 data
    """
    try:
        # 動態生成 footer 的按鈕內容
        buttons = [
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label": btn["label"],
                    "data": btn["data"]
                }
            }
            for btn in foot_btn
        ]

        # 組裝字卡內容
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"【問題{ques_no}】{ques}",
                        "weight": "bold",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": detail,
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
                "contents": buttons
            }
        }

        # 發送字卡訊息
        flex_message = FlexSendMessage(
            alt_text=f"症狀問題{ques_no}",
            contents={
                "type": "carousel",
                "contents": [bubble]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
questions = [
    {
        "ques_no": 1,
        "ques": "您是否有頭暈嘔吐現象?",
        "detail": "這裡放輔助說明的小字",
        "foot_btn": [
            {"label": "有", "data": "action=epro1,有"},
            {"label": "沒有", "data": "action=epro1,沒有"}
        ]
    },
    {
        "ques_no": 2,
        "ques": "您最近3天有腹瀉程度?",
        "detail": "這裡放輔助說明的小字",
        "foot_btn": [
            {"label": "沒有", "data": "action=epro2,沒有"},
            {"label": "普通", "data": "action=epro2,普通"},
            {"label": "超嚴重", "data": "action=epro2,超嚴重"}
        ]
    }
]
def start_epro_ques_1(event, lindId):
    """
    啟動問題1
    """
    question = questions[0]  # 取得問題1
    generate_question_card(
        event,
        ques_no=question["ques_no"],
        ques=question["ques"],
        detail=question["detail"],
        foot_btn=question["foot_btn"]
    )


def start_epro_ques_2(event, lindId):
    """
    啟動問題2
    """
    question = questions[1]  # 取得問題2
    generate_question_card(
        event,
        ques_no=question["ques_no"],
        ques=question["ques"],
        detail=question["detail"],
        foot_btn=question["foot_btn"]
    )

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

def handle_user_registration(event, lineId, user_input=None):
    """
    處理使用者輸入姓名和病歷號的邏輯
    """
    user_track = user_linebot_track.objects.filter(line_id=lineId).first()

    if user_track and not user_track.true_name:
        # 更新 true_name 並要求輸入病歷號
        user_track.true_name = user_input
        user_track.save()
        message = TextSendMessage(text='請輸入您的病歷號：')
        line_bot_api.reply_message(event.reply_token, message)
        return False  # 尚未完成登記

    elif user_track and not user_track.chart_id:
        # 更新 chart_id 並完成登記
        user_track.chart_id = user_input
        user_track.save()
        message = TextSendMessage(
            text=f"✅ 已完成登記：{user_track.true_name}（{user_track.chart_id}）"
        )
        line_bot_api.reply_message(event.reply_token, message)
        return True  # 登記完成

    return False  # 尚未完成登記
def handle_postback(event):
    data = event.postback.data
    lineId = event.source.user_id
    print('\033[93m' + f'handle_postback: {event.postback}' + '\033[0m')
    category, reply = clean_epro_answer(data)

    if category == 'start':
        user_track = user_linebot_track.objects.filter(line_id=lineId).first()
        if user_track and user_track.true_name and user_track.chart_id:
            start_epro_ques_1(event, data)
        else:
            user_linebot_track.objects.update_or_create(
                line_id=lineId,
                defaults={'true_name': '', 'chart_id': ''}
            )
            handle_user_registration(event, lineId)

    elif category == 'epro1':
        start_epro_ques_2(event, data)
        user_linebot_track.objects.create(
            line_id=lineId,
            request=reply,
            category=category
        )

    elif category == 'epro2':
        user_linebot_track.objects.create(
            line_id=lineId,
            request=reply,
            category=category
        )
        message = TextSendMessage(text='作答完畢，感謝配合')
        line_bot_api.reply_message(event.reply_token, message)

    else:
        message = TextSendMessage(text='發生錯誤!')
        line_bot_api.reply_message(event.reply_token, message)
