import uuid
from django.db import models
from django_resized import ResizedImageField

class user_linebot_track(models.Model):
  line_id = models.TextField(blank=True)
  request = models.TextField(default='', blank=True)
  upload = ResizedImageField(upload_to='linebot/', force_format="WEBP", quality=75, null=True, blank=True)
  category = models.TextField(default='system', blank=True)
  true_name = models.TextField(default='', blank=True)
  chart_id = models.TextField(default='', blank=True)
  create_date = models.DateTimeField(auto_now_add=True) # 會自動建立日期

  class Meta:
      db_table = "user_linebot_track" # 輸出table