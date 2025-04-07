# from django.shortcuts import render

# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
import requests
# from django.shortcuts import render, redirect
from chat.models import chat_room, chat_record
import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()

apiTokenUrl = 'https://api.line.me/oauth2/v2.1/token'
apiProfileUrl = 'https://api.line.me/v2/profile'

# 開發
if settings.DEBUG == True:
  LINE_ID = '2006462026'
  LINE_SECRET = '5d9bbfbaeb564b6bae32765e79c20ab2'
  # REDIRECT_URL = 'http://127.0.0.1:3000/'
  REDIRECT_URL = 'http://192.168.50.132:3000/'

# 部屬
else:
  LINE_ID = '2006754723'
  LINE_SECRET = '313b67b3c810351c1396b450ac5c35e0'
  REDIRECT_URL = 'https://wdcare.net/'

# === JWT參考說明 === #
# https://medium.com/%E4%BC%81%E9%B5%9D%E4%B9%9F%E6%87%82%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88/jwt-json-web-token-%E5%8E%9F%E7%90%86%E4%BB%8B%E7%B4%B9-74abfafad7ba
# https://jwt.io/
# https://www.cadch.com/article/timestamp/index.php


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def line_fast_login(request):
  serializer = JSONParser().parse(request)
  code = serializer['code']
  state = serializer['state']

  data_config = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URL,
    'client_id': LINE_ID,
    'client_secret': LINE_SECRET
  }

  lineAuthApi = requests.post(
    apiTokenUrl,
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    data = data_config)
  
  lineAuthResult = lineAuthApi.json()
  access_token = lineAuthResult["access_token"]
  jwtTokenId = lineAuthResult["id_token"]

  # print('SHOW JWT TOKEN', jwtTokenId)
    
  responseProfile = requests.get(
      apiProfileUrl,
      headers = {
          'Authorization': f'Bearer {access_token}',
      },
  )

  getProfileJson = responseProfile.json()

  {
    'userId': 'U98cd6521297c5a714372aabefaef5bc9',
    'displayName': '周子堯 Victor',
    'statusMessage': 'cancell.tw',
    'pictureUrl': 'https://profile.line-scdn.net/0hBArZlfZ8HW5fIwjvDqVjES9zHgR8UkR8JE1UWGl2QVw3EF0wehJRDD10FFgwRglqIUFTWzh0EwxTMGoIQXXhWlgTQF9jFF8_cERRjw'}
  try:
      getMember = User.objects.get(account=getProfileJson['userId'], fast_auth="LINE") # Queryset
      # 更新 last_login 欄位為當前時間
      getMember.last_login = timezone.now() + timedelta(hours=8)
      getMember.save()
      getUserAuthId = getMember.id
      getSuperUser = getMember.is_superuser
      getRoomPath = chat_room.objects.get(user_id=getUserAuthId).room_path
      # print(getRoomPath)
      # return Response('ok', status=200)

  except User.DoesNotExist:
      newUUID4 = uuid.uuid4()
      
      createUser = User.objects.create(
        fast_auth = 'LINE',
        account = getProfileJson['userId'],
        name = getProfileJson['displayName'],
        avatar = getProfileJson['pictureUrl'],
        hashCode = newUUID4,
        last_login=timezone.now() + timedelta(hours=8)  # 新增使用者時設定 last_login
      )

      getUserAuthId = createUser.id
      getSuperUser = createUser.is_superuser

      creatChatRoom = chat_room.objects.create(
        user_id=getUserAuthId,
        room_path=f"{getUserAuthId}-{newUUID4}"
      )
      getRoomPath = creatChatRoom.room_path
      # 增加歡迎詞
      welcome_message = chat_record.objects.create(
          create_user=10,
          content="Welcome! We are Dr. Wound's medical team, here to assist with your wound care needs. Feel free to reach out via text and upload wound photos if needed for better assessment and support. We’re here to help :) 🙂",
          content_type='text',
          is_carer_user=True,
          room_path=getRoomPath
      )

  return Response({
     "status": "ok",
     "jwt_token": jwtTokenId,
     "user_id": getUserAuthId,
     "super_user": getSuperUser,
     "room_path": getRoomPath
  }, status=200)


# Line判斷有無會員資料，存DB
# 新建Model，存LINE id
# 閱讀JWT