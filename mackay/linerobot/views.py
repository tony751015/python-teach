import environ
import os
import uuid

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, actions, events, TemplateSendMessage, PostbackEvent
from linebot.models.messages import StickerMessage

from .models import user_linebot_track
from linerobot import modules

from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

env = environ.Env()
environ.Env.read_env()
LINE_CHANNEL_ACCESS_TOKEN = env('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_ACCESS_SECRET = env('LINE_CHANNEL_ACCESS_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

print('LINE_CHANNEL_ACCESS_TOKEN', LINE_CHANNEL_ACCESS_TOKEN)
print('LINE_CHANNEL_ACCESS_SECRET', LINE_CHANNEL_ACCESS_SECRET)

line_bot_api1 = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_ACCESS_SECRET)

# pip install line-bot-sdk

@csrf_exempt
def line_bot_callback(request):
    if request.method == 'POST':
        signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        # 處理接收到的事件
        for event in events:
            if isinstance(event, MessageEvent):
                # 取得使用者 LINE ID
                lineId = event.source.user_id
                profile = line_bot_api.get_profile(lineId)
                userName = profile.display_name
                pictureUrl = profile.picture_url
                user_input = event.message.text.strip()  # 使用者輸入的文字
                print('User ID:', lineId)
                print('User Name:', userName)
                print('Picture URL:', pictureUrl)

                # 檢查 LINE ID 是否已存在於資料庫
                findUserLineRecord = user_linebot_track.objects.filter(line_id=lineId).exists()
                findUser = User.objects.filter(account=lineId).exists()

                if not findUserLineRecord:
                    user_linebot_track.objects.create(
                        line_id=lineId,
                        request='首次使用紀錄',
                        category='system'
                    )

                if not findUser:
                    # 如果使用者不存在，則新增使用者
                    uuuid = uuid.uuid4()
                    User.objects.create(
                        is_superuser=False,
                        fast_auth='LINE',
                        verify=True,
                        name=userName,
                        account=lineId,
                        hashCode=uuuid,
                        avatar=pictureUrl
                    )

                # 偵測文字訊息
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text.lower().replace('\uff20', '@')

                    # 如果使用者輸入 "@症狀回報"，啟動 ePRO 問卷流程
                    if mtext == '@症狀回報':
                        modules.start_epro(event, lineId)
                        continue  # 跳過後續處理

                # 呼叫 handle_user_registration 處理姓名和病歷號
                if not modules.handle_user_registration(event, lineId, user_input):
                    # 如果尚未完成登記，跳過後續處理
                    continue

                # 如果完成登記，進入 ePRO 問卷流程
                modules.start_epro_ques_1(event, lineId)

            elif isinstance(event, PostbackEvent):
                # 呼叫 handle_postback 處理 Postback 事件
                modules.handle_postback(event)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()