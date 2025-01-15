from mackay.settings import *
print(f'\n=====================================\n**** 已啟用開發模式 [DEBUG TRUE] ****\n=====================================\n')
DEBUG = True
ALLOWED_HOSTS = ['*']
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True