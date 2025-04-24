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
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body,signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        #收到傳送者傳送的訊息 接接收到的訊息傳回.
        for event in events:
            # 判斷是否為縮圖或圖片訊息
            # if isinstance(event, StickerMessage) or event.message.type == 'image':
            #     message = TextSendMessage(text = '提醒您，我們不會針對圖片或貼圖做智能回覆喔。')
            #     line_bot_api.reply_message(event.reply_token,message)
     

            # 一般訊息事件，大部分回應都在這
            if isinstance(event, MessageEvent):
                # 取得使用者LINEID
                lineId = event.source.user_id
                profile = line_bot_api.get_profile(lineId)
                userName = profile.display_name
                pictureUrl = profile.picture_url
                print('User ID:', lineId)
                print('User Name:', userName)
                print('Picture URL:', pictureUrl)
                findUserLineRecord = user_linebot_track.objects.filter(line_id = lineId).count()
                findUser = User.objects.filter(account = lineId).count()

                print('LINE CONFIG', event)

                # 檢查LINEID在資料庫是否存在
                if not findUserLineRecord or not findUser:
                    user_linebot_track.objects.create(
                        line_id = lineId,
                        request = '首次使用紀錄',
                        category = 'system')

                    uuuid = uuid.uuid4()

                    User.objects.create(
                      is_superuser=False,
                      fast_auth='LINE',
                      verify=True,
                      name=userName,
                      account=lineId,
                      hashCode=uuuid,
                      avatar=pictureUrl)
                
                # 偵測到 @xxx 的關鍵字
                if isinstance(event.message,TextMessage):
                    mtext = event.message.text.lower()
                    mtext.replace('\uff20','@')
                    
                    # ==================== linebot_v3 ====================
                    if mtext == '@症狀回報':
                      modules.start_epro(event, lineId)

                    # elif mtext == '@衛教內容':
                    #   modules.start_education(event, lineId)

                    # elif mtext == '@掛號進度':
                    #   modules.start_track_register(event, lineId)
                    # ==================== linebot_v3 end ====================
            elif isinstance(event, PostbackEvent):
                modules.handle_postback(event)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
