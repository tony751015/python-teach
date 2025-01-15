import environ
import os
from pathlib import Path
from google.oauth2 import service_account

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
DOMAIN = env('BASE_DOMAIN')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = [
  '34.80.24.89',
  '34.149.217.42',
  'www.wdcare.net',
  'wdcare.net'
] # 屆時要加入
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    # 下面開始是引用的APP
    'corsheaders',
    "user",
    "chat",
    "ai"
]

# 下面定義會員資料結構來源
AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "mackay.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            FRONTEND_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mackay.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
# STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static') 
STATICFILES_DIRS = [
    FRONTEND_DIR
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # 上傳至GCP Storage，設定會去吃gcpUtils.py檔案
STATICFILES_STORAGE = 'mackay.gcpUtils.Static'
DEFAULT_FILE_STORAGE = 'mackay.gcpUtils.Media'
GS_FILE_OVERWRITE = True

# # 上線部屬的BUCKET路徑
GS_BUCKET_NAME = env('GS_BUCKET_NAME') 
# print('GS_BUCKET_NAME', GS_BUCKET_NAME)
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR, 'gcp-upload.json')) # 本機/Server上內容會不同。
