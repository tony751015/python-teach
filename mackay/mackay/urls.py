from django.contrib import admin
from django.urls import path

from user.views import load_user_profile
from chat.views import chat_record_list, chat_record_control

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("api/user/load_profile", load_user_profile),
    path("api/chat/control", chat_record_control),
    path("api/chat/list", chat_record_list),
]
