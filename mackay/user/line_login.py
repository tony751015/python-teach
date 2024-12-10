# from django.shortcuts import render

# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
import requests
# from django.shortcuts import render, redirect
from chat.models import chat_room
import uuid
from django.utils import timezone
from datetime import timedelta
# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()

apiTokenUrl = 'https://api.line.me/oauth2/v2.1/token'
apiProfileUrl = 'https://api.line.me/v2/profile'

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
    'redirect_uri': 'http://127.0.0.1:3000/',
    'client_id': 2006462026,
    'client_secret': '5d9bbfbaeb564b6bae32765e79c20ab2'
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

  print('SHOW JWT TOKEN', jwtTokenId)
    
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

      chat_room.objects.create(
        user_id=getUserAuthId,
        room_path=f"{getUserAuthId}-{newUUID4}"
      )

  return Response({
     "status": "ok",
     "jwt_token": jwtTokenId,
     "user_id": getUserAuthId,
     "super_user": getSuperUser
  }, status=200)


# Line判斷有無會員資料，存DB
# 新建Model，存LINE id
# 閱讀JWT