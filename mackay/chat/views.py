# from django.shortcuts import render
# 引用rest_framework相關功能
from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db.models.functions import TruncDate
# 抓取chat的 model.py 的 chat_record table
from .models import chat_record, chat_room
from django.db.models import Q, F, Func, Value, CharField
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from mackay.settings import DEBUG

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
  try:
    # serializer = JSONParser().parse(request)
    serializer = request.GET

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

      try:
        findChatRoom = chat_room.objects.get(user_id=user_id)
      except chat_room.DoesNotExist:
        return Response('no found', status=404)
      except:
        return Response('error', status=404)
      
      chatRoomPath = findChatRoom.room_path
      recordCount = recordQuery.count() # 找到的資料數量
      # recordData = recordQuery.order_by('-create_date').annotate(record_id=F('id')).values_list('record_id', 'content', 'content_type', 'create_date', 'is_carer_user') # 取出指定Field

      # 把recordQuery資料集先判斷create_date_truncated的順序作排列 (最新到舊)
      # 排序完後，在轉換id成自己希望的key name = record_id
      # 然後再取出想給前端的資料
      filterData = recordQuery.order_by('create_date').values_list('create_date_truncated', flat=True)
      # check2 = check1.order_by('-create_date_truncated')

      # recordData = list(recordQuery.values_list('create_date_truncated', flat=True).order_by('-create_date_truncated').annotate(record_id=F('id')).values('record_id', 'content', 'content_type', 'create_date_truncated', 'is_carer_user'))
      recordData = list(filterData.annotate(record_id=F('id')).values('record_id', 'content', 'media_url', 'content_type', 'create_date_truncated', 'is_carer_user'))

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
        

      #   # 轉換格式
      #   newDateTime = oldDate.strftime('%Y-%m-%d') # 轉換格式 YYYY-MM-DD
      #   # 每筆資料額外添加 user_name / gender的資料
      #   items['user_name'] = getUserName
      #   items['gender'] = getUserGender
      #   # 替換原本create_date的資料內容
      #   items['create_date'] = newDateTime
      # 反轉 recordData
        recordData = list(reversed(recordData))
      try:
        p = Paginator(recordData, size) 
        page1 = p.page(page)
        final = page1.object_list
        results = {
          "count": recordCount,
          "room_path": chatRoomPath,
          "results": final
        }
        return Response(results, status=200)
      
      # 如果超出分頁範圍
      except PageNotAnInteger:
        results = {
          "count": recordCount,
          "room_path": chatRoomPath,
          "results": []
        }
        return Response(results, status=200)

      # 如果指定分頁沒有資料
      except EmptyPage:
        results = {
          "count": recordCount,
          "room_path": chatRoomPath,
          "results": []
        }
        return Response(results, status=200)
      
      # 發生其他錯誤時
      except:
        return Response('error 1', status=500)
      
    else:
      return Response('need params', status=500)
    
  except Exception as e:
    return Response(e, status=500)
    



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
    


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def chat_upload_photo(request):
  resData = request.data
  create_user = resData["user_id"]
  isCarerUser = resData["is_carer_user"]
  # photo_upload1 = request.FILES.get('photo_upload')
  photo_upload = request.FILES['photo_upload']

  # create_date = datetime.now().strftime("%Y-%m-%d")

  if 'user_id' in resData and 'is_carer_user' in resData:
    # # try:
    # isPatient = False

    # if isCarerUser == '0':
    #   isPatient = True
    
    createNewRecord = chat_record.objects.create(
      create_user = create_user,
      content = '',
      content_type = 'image',
      media_url = photo_upload,
      is_carer_user = isCarerUser,
    )
    if createNewRecord:
      createNewRecordId = createNewRecord.id

      return Response({
        "status": "create",
        "record_id": createNewRecordId,
      }, status=200)
    # except:
    #   # 遇到任何問題則回傳error
    #   return Response('error', status=500)
  else:
    return Response('error', status=500)



  # savePhotoUrls = []
  # # print('settings.GS_BUCKET_NAME', settings.GS_BUCKET_NAME)
  # for img in photo_upload:
  #   savePhoto = se_photo_upload.objects.create(attribute='se_report_translate', src=img)
  #   saveReport.upload.add(savePhoto)
  #   savePhotoUrls.append(f'https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/media/{str
  #                                                                                          (savePhoto.src)}')

@api_view(['GET', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def chat_record_photo(request):
    if request.method == 'GET':
        try:
            # 解析GET請求中的參數
            serializer = request.GET
            user_id = serializer['user_id']
            page = serializer['page']
            size = serializer['size']

            # 檢查是否有提供必要的參數
            if user_id or page or size:
                # 取得某會員的圖片對話記錄，並使用TruncDate來截斷日期
                recordQuery = chat_record.objects.filter(
                    Q(create_user=user_id) & Q(content_type='image')
                ).annotate(
                    create_date_truncated=TruncDate('create_date')
                )

                try:
                    # 嘗試取得該會員的聊天室路徑
                    findChatRoom = chat_room.objects.get(user_id=user_id)
                except chat_room.DoesNotExist:
                    # 如果找不到聊天室，回傳404
                    return Response('no found', status=404)
                except:
                    # 其他錯誤，回傳404
                    return Response('error', status=404)

                # 取得聊天室路徑和記錄數量
                chatRoomPath = findChatRoom.room_path
                recordCount = recordQuery.count()

                # 排序資料並取得需要的欄位
                filterData = recordQuery.order_by('-create_date').values_list('create_date_truncated', flat=True)
                recordData = list(filterData.annotate(record_id=F('id')).values('record_id', 'media_url', 'is_carer_user' ,'create_date_truncated'))

                # 設定一個變數來追蹤當前迴圈的日期
                currentLoopDate = ''

                # 迴圈處理每一筆資料
                for items in recordData:
                    itemsDate = items['create_date_truncated']
                    # 如果當前日期與上次迴圈的日期不同，標記為isFirstDate
                    if currentLoopDate != itemsDate:
                        items['isFirstDate'] = itemsDate
                    else:
                        items['isFirstDate'] = ''
                    # 更新currentLoopDate為當前日期
                    currentLoopDate = itemsDate

                try:
                    # 使用Paginator進行分頁
                    p = Paginator(recordData, size)
                    current_page = p.page(page)
                    final = current_page.object_list
                    results = {
                        "count": recordCount,
                        "room_path": chatRoomPath,
                        "results": final
                    }
                    return Response(results, status=200)

                except PageNotAnInteger:
                    # 如果頁碼不是整數，回傳空結果
                    results = {
                        "count": recordCount,
                        "room_path": chatRoomPath,
                        "results": []
                    }
                    return Response(results, status=200)

                except EmptyPage:
                    # 如果頁面超出範圍，回傳空結果
                    results = {
                        "count": recordCount,
                        "room_path": chatRoomPath,
                        "results": []
                    }
                    return Response(results, status=200)

                except:
                    # 其他錯誤，回傳500
                    return Response('error 1', status=500)

            else:
                # 如果缺少必要參數，回傳500
                return Response('need params', status=500)

        except Exception as e:
            # 捕捉所有其他例外，回傳500
            return Response(e, status=500)

    elif request.method == 'DELETE':
        try:
            # 解析DELETE請求中的參數
            serializer = request.data
            record_id = serializer.get('record_id')
            user_id = serializer.get('user_id')  # 單個user_id

            if record_id and user_id:
                try:
                    # 使用record_id和user_id進行過濾
                    record = chat_record.objects.get(id=record_id, content_type='image', create_user=user_id)
                    record.delete()
                    return Response('deleted', status=200)
                except chat_record.DoesNotExist:
                    return Response('record not found', status=404)
                except:
                    return Response('error', status=500)
            else:
                return Response('need record_id and user_id', status=400)

        except Exception as e:
            return Response(e, status=500)