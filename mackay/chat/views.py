# from django.shortcuts import render
# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
# 抓取chat的 model.py 的 chat_record table
from .models import chat_record
from django.db.models import Q, F
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def chat_record_list(request):
  serializer = JSONParser().parse(request)
  
  # 如果有找到params
  if 'user_id' and 'page' and 'size' in serializer:
    userId = serializer['user_id']
    page = serializer['page']
    size = serializer['size']

    # 取得某會員 指定Field的對話記錄 
    recordQuery = chat_record.objects.filter(Q(create_user=userId))
    recordCount = recordQuery.count() # 找到的資料數量
    recordData = recordQuery.order_by('-create_date').annotate(record_id=F('id')).values('record_id', 'content', 'content_type', 'create_date') # 取出指定Field


  
    # For迴圈
    for items in recordData:
      eachUserId = User.objects.get(id=userId) # 取得每筆資料的User檔案，因為id是唯一，所以用GET
      getUserName = eachUserId.name # 會員名稱
      getUserGender = eachUserId.gender # 會員性別
      oldDate = items['create_date'] # 先記錄原本日期

      # 轉換格式
      newDateTime = oldDate.strftime('%Y-%m-%d') # 轉換格式 YYYY-MM-DD
      # 每筆資料額外添加 user_name / gender的資料
      items['user_name'] = getUserName
      items['gender'] = getUserGender
      # 替換原本create_date的資料內容
      items['create_date'] = newDateTime

    try:
      p = Paginator(recordData, size) 
      page1 = p.page(page)
      final = page1.object_list 
      results = {
        "count": recordCount,
        "results": final
      }
      return Response(results, status=200)
    
    # 如果超出分頁範圍
    except PageNotAnInteger:
      results = {
        "count": recordCount,
        "results": []
      }
      return Response(results, status=200)

    # 如果指定分頁沒有資料
    except EmptyPage:
      results = {
        "count": recordCount,
        "results": []
      }
      return Response(results, status=200)
    
    # 發生其他錯誤時
    except:
      return Response('error', status=500)
    
  else:
    return Response('need params', status=500)
    



@api_view(['POST', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def chat_record_control(request):
  serializer = JSONParser().parse(request)

  if request.method == 'DELETE':
    if 'record_id' in serializer:
      recordId = serializer['record_id']

      # try:
      #   getRecord = chat_record.objects.get(id=recordId)
      #   getRecord.delete()
      #   return Response('delete', status=200)
      
      # # 如果找不到該筆對話記錄
      # except chat_record.DoesNotExist:
      #   return Response('error', status=500)
      
      # # 其他錯誤發生
      # except:
      #   return Response('error', status=500)

      try:
        getManyRecord = chat_record.objects.filter(Q(content_type='text')).delete() # 全部都刪除
        return Response('delete', status=200)
      except:
        return Response('error', status=500)
      
    

  elif request.method == 'PUT':
    if 'record_id' in serializer:
      recordId = serializer['record_id']
      updateContent = serializer['content']

      # 如果是找單筆資料，而且確定這筆資料獨一無二，用id去找
      # try:
      #   getRecord = chat_record.objects.get(id=recordId)
      #   getRecord.content = updateContent
      #   getRecord.save()
      #   return Response('update', status=200)
      
      # # 如果找不到該筆對話記錄
      # except chat_record.DoesNotExist:
      #   return Response('error', status=500)
      
      # # 其他錯誤發生
      # except:
      #   return Response('error', status=500)
      
    

      # 如果是找多筆資料，用content_type去找
      try:
        getManyRecord = chat_record.objects.filter(Q(content_type='text'))
        getManyRecord.update(content=updateContent) # 全部都更新
        return Response('update', status=200)
      except:
        return Response('error', status=500)

    else:
      return Response('need params', status=500)


  elif request.method == 'POST':
    # 檢查是否有email params
    try:
      if 'user_id' in serializer and 'content' in serializer:
        getUserId = serializer['user_id']
        getContent = serializer['content']
        contentType = serializer['content_type']
        # 建立一筆新資料
        # 如果沒有default值，則必須傳參數
        newCreate = chat_record.objects.create(
          create_user = getUserId,
          content = getContent,
          content_type = contentType)
        
        if newCreate:
          return Response({
            "status": "create",
            "record_id": newCreate.id
          }, status=200)
      
      # 如果沒有params 回傳500 error 錯誤訊息
      else:
        return Response('need params', status=500)
      
    except:
       # 遇到任何問題則回傳error
       return Response('error', status=500)
  else:
    return Response('error', status=500)
    
