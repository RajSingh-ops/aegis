from django.urls import re_path
from .consumers import AuditorConsumer

websocket_urlpatterns = [
    re_path(r'ws/auditor/$', AuditorConsumer.as_asgi()),
]
