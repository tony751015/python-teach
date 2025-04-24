from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
# from user.views import load_user_profile, load_member_list_ssr, load_member_list_ssr_query
from user.views import user_fast_login, load_user_chat_room, chat_room_update_pin, chat_room_update_ban
from user.line_login import line_fast_login
from chat.views import chat_record_list, chat_record_control, chat_record_ssr, chat_record_ssr_with_query, chat_upload_photo, chat_record_photo

from ssr.views import index_ssr, chat_ssr, chat_room_ssr

from ai.views import gemini_request
from linerobot.views import line_bot_callback

from django.views.static import serve
from django.urls import re_path as url

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("api/user/load_profile", load_user_profile),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    path("api/chat/control", chat_record_control),
    path("api/chat/list", chat_record_list),
    path("api/chat/photo", chat_record_photo),
    path("api/chat/upload", chat_upload_photo),
    path("api/chat/room", load_user_chat_room),
    path("api/chat/update_pin", chat_room_update_pin),
    path("api/chat/update_ban", chat_room_update_ban),

    path("", index_ssr),
    re_path(r'chat\/?$', chat_ssr),
    path('chat/<room>', chat_room_ssr),

    path("api/member/fast_login", user_fast_login),
    path("api/member/line_login", line_fast_login),

    path("api/ai/gemini_request", gemini_request),
    # path("member/", load_member_list_ssr),
    # path("member/<id>", load_member_list_ssr_query),

    # LINEBOT MESSAGE API
    path("api/line/callback", line_bot_callback),

    path('mvc/', chat_record_ssr), # 執行 chat_record_ssr
    path('mvc/<id>', chat_record_ssr_with_query), # 執行 chat_record_ssr_with_query
    # path('', TemplateView.as_view(template_name='index.html')), # 如果無特殊任務，直接渲染靜態網頁
    re_path('^.*$', TemplateView.as_view(template_name='index.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#     re_path('^.*$', TemplateView.as_view(template_name='index.html')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL + 'chat/', document_root=settings.MEDIA_ROOT + '/chat/')