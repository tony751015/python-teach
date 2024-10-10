# from django.shortcuts import render

# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
from chat.models import chat_room
import uuid

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
  


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_fast_login(request):
  serializer = JSONParser().parse(request)

  if 'patient_id' in serializer and 'patient_name' in serializer and 'patient_auth' in serializer:
    patient_id = serializer["patient_id"]
    patient_name = serializer["patient_name"]
    patient_auth = serializer["patient_auth"]
    # line_thumb = serializer["line_thumb"]
    # print('user_fast_login', serializer)
    
    try:
      User.objects.get(account=patient_id, fast_auth=patient_auth)
      # getMember = User.objects.get(account=patient_id, fast_auth=patient_auth)
      # getMemberList = list(getMember)
      # ctx = {
      #   "load_member_list_ssr": getMemberList
      # }
      return Response('is exist', status=200)

    except User.DoesNotExist:
      newUUID4 = uuid.uuid4()
      
      createUser = User.objects.create(
        fast_auth= patient_auth,
        account=patient_id,
        name=patient_name,
        hashCode = newUUID4,
      )

      newCreateID = createUser.id

      chat_room.objects.create(
        user_id=newCreateID,
        room_path=f"{newCreateID}-{newUUID4}"
      )
      # getMember = User.objects.get(account=patient_id, fast_auth=patient_auth)
      # getMemberList = list(getMember)
      # ctx = {
      #   "load_member_list_ssr": getMemberList
      # }
      return Response('new create', status=200)

    # obj, created = User.objects.get_or_create(
    #     # fast_auth = patient_auth,
    #     account = patient_id,
    #     hashCode = uuid.uuid4(),
    #     name = patient_name,
    #     defaults = {
    #         'account': patient_id,
    #         'fast_auth': "LINE"
    #     }
    # )

    # if created:
    #   return Response('new create', status=200)
    
    # elif obj:
    #   return Response({
    #     "status": "is exist",
    #     "data": obj
    #   }, status=200)
  
  else: 
    return Response('error', status=400)

  

