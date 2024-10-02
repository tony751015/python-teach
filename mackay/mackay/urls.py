from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

# from user.views import load_user_profile, load_member_list_ssr, load_member_list_ssr_query
from user.views import user_fast_login
from chat.views import chat_record_list, chat_record_control, chat_record_ssr, chat_record_ssr_with_query

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("api/user/load_profile", load_user_profile),
    path("api/chat/control", chat_record_control),
    path("api/chat/list", chat_record_list),

    path("api/member/fast_login", user_fast_login),
    # path("member/", load_member_list_ssr),
    # path("member/<id>", load_member_list_ssr_query),

    path('mvc/', chat_record_ssr), # 執行 chat_record_ssr
    path('mvc/<id>', chat_record_ssr_with_query), # 執行 chat_record_ssr_with_query
    path('', TemplateView.as_view(template_name='index.html')), # 如果無特殊任務，直接渲染靜態網頁
]
