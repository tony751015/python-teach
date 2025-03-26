from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
import os

# pip install line-bot-sdk

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def send_bubble_message(event):
  try:
    bubble = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "",
            "size": "full",
            "aspectRatio": "13:9",
            "aspectMode": "cover",
          },
          {
            "type": "text",
            "text": "TEXT",
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "text",
            "text": "TEXT。",
            "weight": "bold",
            "size": "sm",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "TEXT",
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
                "type": "uri",
                "label": "TEXT",
                "uri": ""
              }
            },
            {
              "type": "button",
              "style": "primary",
              "action": {
                "type": "uri",
                "label": "TEXT",
                "uri": ""
              }
            }
          ]
        }
    }

    flex_message = FlexSendMessage(
      alt_text="ALT_TEXT",
      contents={
        "type": "carousel",
        "contents": [bubble]
      }
    )
    line_bot_api.reply_message(event.reply_token, flex_message)
  except Exception as e:
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))


def send_text_message(event):
  try:
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text = "TEXT"))
  except Exception as e:
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤!'))

# send_bubble_message()
