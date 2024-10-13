# from django.shortcuts import render
# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db.models.functions import TruncDate
# 抓取chat的 model.py 的 chat_record table
from .models import chat_record
from django.db.models import Q, F, Func, Value, CharField
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()


# URLpath: mvc/
def chat_record_ssr(request):
  recordData = chat_record.objects.all()
  recordDataList = list(recordData)
  ctx = {
    "chat_record_ssr": recordDataList
  }
  return render(request, "mvc.html", ctx)



# URLpath: mvc/<id>
def chat_record_ssr_with_query(request, id):
  recordData = chat_record.objects.filter(Q(id=id))
  recordDataList = list(recordData)
  ctx = {
    "chat_record_ssr_with_query": id
  }
  return render(request, "mvc.html", ctx)


# GET / POST / DELETE = request.data
# JSONParser().parse(request)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def chat_record_list(request):
  # try:
    serializer = JSONParser().parse(request)
    # serializer = request.GET

    # user_id = serializer.get('user_id')
    # page = serializer.get('page', 1)
    # size = serializer.get('size', 10)
    user_id = serializer['user_id']
    page = serializer['page']
    size = serializer['size']

    # 如果有找到params
    if user_id or page or size:

      # 取得某會員 指定Field的對話記錄
      # Filter後先使用annotate + TruncDate，設計一個新的資料key = create_date_truncated，轉換create_date成 2024-10-01格式
      recordQuery = chat_record.objects.filter(Q(create_user=user_id)).annotate(
        create_date_truncated=TruncDate('create_date')
      )
      recordCount = recordQuery.count() # 找到的資料數量
      # recordData = recordQuery.order_by('-create_date').annotate(record_id=F('id')).values_list('record_id', 'content', 'content_type', 'create_date', 'is_carer_user') # 取出指定Field

      # 把recordQuery資料集先判斷create_date_truncated的順序作排列 (最新到舊)
      # 排序完後，在轉換id成自己希望的key name = record_id
      # 然後再取出想給前端的資料
      recordData = list(recordQuery.values_list('create_date_truncated', flat=True).order_by('-create_date_truncated').annotate(record_id=F('id')).values('record_id', 'content', 'content_type', 'create_date_truncated', 'is_carer_user'))

      # 設計一個變數，用來記錄每次For迴圈保存的 create_date_truncated 值
      currentLoopDate = ''

      # For迴圈
      for items in recordData:
        itemsDate = items['create_date_truncated']

        # 比對上一輪Loop的currentLoopDate 是否跟 當前create_date_truncated 相同?
        # 如果不相同，把當前日期寫入 isFirstDate
        # 否則 isFirstDate 寫入空值
        if currentLoopDate != itemsDate:
          items['isFirstDate'] = itemsDate
        else: 
          items['isFirstDate'] = ''

        # 上面完成後 在更新currentLoopDate 為當前Loop日期
        currentLoopDate = itemsDate

        eachUserId = User.objects.get(id=user_id) # 取得每筆資料的User檔案，因為id是唯一，所以用GET
        getUserName = eachUserId.name # 會員名稱
        getUserGender = eachUserId.gender # 會員性別
        # 每筆資料額外添加 user_name / gender的資料
        items['user_name'] = getUserName
        items['gender'] = getUserGender
        # 替換原本create_date的資料內容

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
    
  # except:
  #   return Response('error', status=500)
    



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
    
    # print('Check 1', request)
    try:
     
      if 'user_id' in serializer and 'content' in serializer:
        getUserId = serializer['user_id']
        getContent = serializer['content']
        contentType = serializer['content_type']
        isCarerUser = serializer['is_carer_user']
        # 建立一筆新資料
        # 如果沒有default值，則必須傳參數
        newCreate = chat_record.objects.create(
          create_user = getUserId,
          content = getContent,
          content_type = contentType,
          is_carer_user = isCarerUser)
        
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
    
