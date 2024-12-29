from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
# from user.views import load_user_profile, load_member_list_ssr, load_member_list_ssr_query
from user.views import user_fast_login, load_user_chat_room, chat_room_update_pin
from user.line_login import line_fast_login
from chat.views import chat_record_list, chat_record_control, chat_record_ssr, chat_record_ssr_with_query, chat_upload_photo, chat_record_photo

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("api/user/load_profile", load_user_profile),
    path("api/chat/control", chat_record_control),
    path("api/chat/list", chat_record_list),
    path("api/chat/photo", chat_record_photo),
    path("api/chat/upload", chat_upload_photo),
    path("api/chat/room", load_user_chat_room),
    path("api/chat/update_pin", chat_room_update_pin),

    path("api/member/fast_login", user_fast_login),
    path("api/member/line_login", line_fast_login),
    # path("member/", load_member_list_ssr),
    # path("member/<id>", load_member_list_ssr_query),

    path('mvc/', chat_record_ssr), # 執行 chat_record_ssr
    path('mvc/<id>', chat_record_ssr_with_query), # 執行 chat_record_ssr_with_query
    path('', TemplateView.as_view(template_name='index.html')), # 如果無特殊任務，直接渲染靜態網頁
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path('^.*$', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL + 'chat/', document_root=settings.MEDIA_ROOT + '/chat/')