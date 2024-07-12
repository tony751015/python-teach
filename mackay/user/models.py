from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    email = models.TextField(max_length=50, unique=True)
    name = models.TextField(max_length=50, blank=True)
    birth = models.DateField(auto_now_add=True) # 預設日期是今天
    gender = models.TextField(max_length=50, blank=True)
    fast_auth = models.TextField(max_length=200, blank=True)
    phone = models.TextField(max_length=20, blank=True)
    verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # 主要判斷帳號的資料，作為帳號判斷 必須訂為unique

    @property
    def is_staff(self):
        return 1
    
    objects = UserManager()

    class Meta:
        db_table = 'user' # 最後輸出table的命名