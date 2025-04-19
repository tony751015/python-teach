import uuid
from django.db import models
from django_resized import ResizedImageField

uuuid = uuid.uuid4()

class chat_record(models.Model):
  create_user = models.TextField(blank=True)
  room_path = models.TextField(default='text', blank=True)
  is_carer_user = models.BooleanField(default=False)  # 是否為照護者用戶
  content = models.TextField(default='', blank=True)
  content_type = models.TextField(default='text', blank=True) # 預設text
  ban = models.BooleanField(default=False) # 預設False
  # media_url = models.FileField(upload_to='chat/', default="", null=True, blank=True)
  media_url = ResizedImageField(upload_to='chat/', force_format="WEBP", quality=75, null=True, blank=True)
  message_id = models.UUIDField(default=uuuid, editable=False)
  create_date = models.DateTimeField(auto_now_add=True) # 會自動建立日期

  class Meta:
      db_table = "chat_record" # 輸出table


class chat_room(models.Model):
  user_id = models.TextField(blank=True)
  room_path = models.TextField(default='text', blank=True)
  pin = models.BooleanField(default=False)
  ban = models.BooleanField(default=False)
  create_date = models.DateTimeField(auto_now_add=True) # 會自動建立日期

  class Meta:
      db_table = "chat_room" # 輸出table
