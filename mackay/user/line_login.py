# from django.shortcuts import render

# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
import requests
# from django.shortcuts import render, redirect
from chat.models import chat_room
import uuid

# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()

apiTokenUrl = 'https://api.line.me/oauth2/v2.1/token'
apiProfileUrl = 'https://api.line.me/v2/profile'


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
    'redirect_uri': 'http://127.0.0.1:3000/WoundChat',
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
  print('AAAAAAAAAAAAAAAAAAAAA', lineAuthResult)


  access_token = lineAuthResult["access_token"]
    
  responseProfile = requests.get(
      apiProfileUrl,
      headers = {
          'Authorization': f'Bearer {access_token}',
      },
  )

  getProfileJson = responseProfile.json()

  print('BBBBBBBBBBBBBBBB', getProfileJson)
  {
    'userId': 'U98cd6521297c5a714372aabefaef5bc9',
    'displayName': '周子堯 Victor',
    'statusMessage': 'cancell.tw',
    'pictureUrl': 'https://profile.line-scdn.net/0hBArZlfZ8HW5fIwjvDqVjES9zHgR8UkR8JE1UWGl2QVw3EF0wehJRDD10FFgwRglqIUFTWzh0EwxTMGoIQXXhWlgTQF9jFF8_cERRjw'}
  try:
      getMember = User.objects.get(account=getProfileJson['userId'], fast_auth="LINE") # Queryset


      print('AAAAAAAA', getMember)

      return Response('ok', status=200)

  except User.DoesNotExist:
      newUUID4 = uuid.uuid4()
      
      createUser = User.objects.create(
        fast_auth = 'LINE',
        account = getProfileJson['userId'],
        name = getProfileJson['displayName'],
        avatar = getProfileJson['pictureUrl'],
        hashCode = newUUID4,
      )

      newCreateID = createUser.id

      print('BBBBBBBB', newCreateID)

      chat_room.objects.create(
        user_id=newCreateID,
        room_path=f"{newCreateID}-{newUUID4}"
      )

  return Response('ok', status=200)


# Line判斷有無會員資料，存DB
# 新建Model，存LINE id
# 閱讀JWT