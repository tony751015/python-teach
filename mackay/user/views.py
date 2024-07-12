# from django.shortcuts import render

# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def load_user_profile(request):
  serializer = JSONParser().parse(request)


  # 如果接受到的request方法是 GET
  if request.method == 'GET':
    # 檢查是否有email params
    if 'email' in serializer['email']:
      getEmail = serializer['email']

      # 先簡單測試一下當成功時會回傳email
      print('Check Email', getEmail)
      return Response(getEmail, status=200)
    # 如果沒有 email 回傳500 error 錯誤訊息
    else:
      return Response('need params', status=500)
    
  else:
    return Response('error', status=500)
    
