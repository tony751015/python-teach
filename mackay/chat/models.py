from django.db import models

class chat_record(models.Model):
  create_user = models.TextField(blank=True)
  content = models.TextField(default='', blank=True)
  content_type = models.TextField(default='text', blank=True) # 預設text
  ban = models.BooleanField(default=False) # 預設False
  media_url = models.FileField(upload_to='chat/', default="", null=True, blank=True)
  create_date = models.DateTimeField(auto_now_add=True) # 會自動建立日期

  class Meta:
      db_table = "chat_record" # 輸出table