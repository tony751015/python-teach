from django.urls import path
from . import views

"""
chatTranslate app 的 URL 配置
提供翻譯功能的 API 端點和測試頁面
"""

app_name = 'chatTranslate'

urlpatterns = [
    # API 端點
    path('api/translate/', views.translate_chat_message, name='translate_message'),
    path('api/translate/records/', views.get_translation_records, name='translation_records'),
    
    # 測試頁面
    path('test/', views.test_translation_view, name='test_translation'),
]
