import uuid
from django.db import models
from django_resized import ResizedImageField

class wound_recognize(models.Model):
  create_user = models.TextField(blank=True)
  token_used = models.IntegerField(default=0)
  summary = models.TextField(default='', blank=True)
  ban = models.BooleanField(default=False) # 預設False
  photo_url = ResizedImageField(upload_to='chat/', force_format="WEBP", quality=75, null=True, blank=True)
  create_date = models.DateTimeField(auto_now_add=True) # 會自動建立日期

  class Meta:
      db_table = "wound_recognize" # 輸出table

