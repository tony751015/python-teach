# from django.shortcuts import render

# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect

# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()


# 渲染會員資料的任務
def load_member_list_ssr(request):
  getMember = User.objects.all()
  getMemberList = list(getMember)
  
  ctx = {
    "load_member_list_ssr": getMemberList
  }
  return render(request, "member.html", ctx)


# 渲染某個會員資料的任務
def load_member_list_ssr_query(request, id):
  try:
    getPerMember = User.objects.get(id=id)
  except User.DoesNotExist:
    getPerMember = "error"

  ctx = {
    "load_member_list_ssr_query": getPerMember
  }

  return render(request, "member.html", ctx)




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
  

  
    
