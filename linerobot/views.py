import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定 Line Bot API
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@csrf_exempt
@require_POST
def callback(request):
    # 獲取 X-Line-Signature header 值
    signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')

    # 獲取請求內容
    body = request.body.decode('utf-8')

    try:
        # 驗證簽名
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    return HttpResponse('OK')

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # 獲取用戶發送的訊息
    user_message = event.message.text
    
    # 回覆相同的訊息
    reply_message = user_message
    
    # 發送回覆
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    ) 